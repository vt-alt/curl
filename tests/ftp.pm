#***************************************************************************
#                                  _   _ ____  _
#  Project                     ___| | | |  _ \| |
#                             / __| | | | |_) | |
#                            | (__| |_| |  _ <| |___
#                             \___|\___/|_| \_\_____|
#
# Copyright (C) 1998 - 2009, Daniel Stenberg, <daniel@haxx.se>, et al.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution. The terms
# are also available at http://curl.haxx.se/docs/copyright.html.
#
# You may opt to use, copy, modify, merge, publish, distribute and/or sell
# copies of the Software, and permit persons to whom the Software is
# furnished to do so, under the terms of the COPYING file.
#
# This software is distributed on an "AS IS" basis, WITHOUT WARRANTY OF ANY
# KIND, either express or implied.
#
# $Id: ftp.pm,v 1.18 2009-12-19 13:20:07 yangtse Exp $
###########################################################################

#######################################################################
# pidfromfile returns the pid stored in the given pidfile.  The value
# of the returned pid will never be a negative value. It will be zero
# on any file related error or if a pid can not be extracted from the
# given file.
#
sub pidfromfile {
    my $pidfile = $_[0];
    my $pid = 0;

    if(-f $pidfile && -s $pidfile && open(PIDFH, "<$pidfile")) {
        $pid = 0 + <PIDFH>;
        close(PIDFH);
        $pid = 0 unless($pid > 0);
    }
    return $pid;
}

#######################################################################
# processexists checks if a process with the pid stored in the given
# pidfile exists and is alive. This will return 0 on any file related
# error or if a pid can not be extracted from the given file. When a
# process with the same pid as the one extracted from the given file
# is currently alive this returns that positive pid. Otherwise, when
# the process is not alive, will return the negative value of the pid.
#
sub processexists {
    use POSIX ":sys_wait_h";
    my $pidfile = $_[0];

    # fetch pid from pidfile
    my $pid = pidfromfile($pidfile);

    if($pid > 0) {
        # verify if currently alive
        if(kill(0, $pid)) {
            return $pid;
        }
        else {
            # get rid of the certainly invalid pidfile
            unlink($pidfile) if($pid == pidfromfile($pidfile));
            # reap its dead children, if not done yet
            # waitpid($pid, &WNOHANG);
            # negative return value means dead process
            return -$pid;
        }
    }
    return 0;
}

#######################################################################
# killpid attempts to gracefully stop processes in the given pid list
# with a SIGTERM signal and SIGKILLs those which haven't died on time.
#
sub killpid {
    use POSIX ":sys_wait_h";
    my ($verbose, $pidlist) = @_;
    my @requested;
    my @signalled;
    my @reapchild;

    # The 'pidlist' argument is a string of whitespace separated pids.
    return if(not defined($pidlist));

    # Make 'requested' hold the non-duplicate pids from 'pidlist'.
    @requested = split(' ', $pidlist);
    return if(not defined(@requested));
    if(scalar(@requested) > 2) {
        @requested = sort({$a <=> $b} @requested);
    }
    for(my $i = scalar(@requested) - 2; $i >= 0; $i--) {
        if($requested[$i] == $requested[$i+1]) {
            splice @requested, $i+1, 1;
        }
    }

    # Send a SIGTERM to processes which are alive to gracefully stop them.
    foreach my $tmp (@requested) {
        chomp $tmp;
        if($tmp =~ /^(\d+)$/) {
            my $pid = $1;
            if($pid > 0) {
                if(kill(0, $pid)) {
                    print("RUN: Process with pid $pid signalled to die\n")
                        if($verbose);
                    kill("TERM", $pid);
                    push @signalled, $pid;
                }
                else {
                    print("RUN: Process with pid $pid already dead\n")
                        if($verbose);
                    push @reapchild, $pid;
                }
            }
        }
    }

    # Allow all signalled processes five seconds to gracefully die.
    if(defined(@signalled)) {
        my $twentieths = 5 * 20;
        while($twentieths--) {
            for(my $i = scalar(@signalled) - 1; $i >= 0; $i--) {
                my $pid = $signalled[$i];
                if(!kill(0, $pid)) {
                    print("RUN: Process with pid $pid gracefully died\n")
                        if($verbose);
                    splice @signalled, $i, 1;
                    push @reapchild, $pid;
                }
            }
            last if(not scalar(@signalled));
            select(undef, undef, undef, 0.05);
        }
    }

    # Mercilessly SIGKILL processes still alive.
    if(defined(@signalled)) {
        foreach my $pid (@signalled) {
            if($pid > 0) {
                print("RUN: Process with pid $pid forced to die with SIGKILL\n")
                    if($verbose);
                kill("KILL", $pid);
                push @reapchild, $pid;
            }
        }
    }

    # Reap processes dead children.
    if(defined(@reapchild)) {
        foreach my $pid (@reapchild) {
            if($pid > 0) {
                waitpid($pid, 0);
            }
        }
    }
}

#############################################################################
# Kill a specific slave
#
sub ftpkillslave {
    my ($id, $ext, $verbose)=@_;
    my $base;
    my $pidlist;
    my @pidfiles;

    for $base (('filt', 'data')) {
        my $f = ".sock$base$id$ext.pid";
        my $pid = processexists($f);
        if($pid > 0) {
            printf ("* kill pid for %s => %d\n", "ftp-$base$id$ext", $pid)
                if($verbose);
            $pidlist .= "$pid ";
        }
        push @pidfiles, $f;
    }

    killpid($verbose, $pidlist);

    foreach my $pidfile (@pidfiles) {
        unlink($pidfile);
    }
}

#############################################################################
# Make sure no FTP leftovers are still running. Kill all slave processes.
# This uses pidfiles since it might be used by other processes.
#
sub ftpkillslaves {
    my ($verbose) = @_;
    my $pidlist;
    my @pidfiles;

    for $ext (('', 'ipv6')) {
        for $id (('', '2')) {
            for $base (('filt', 'data')) {
                my $f = ".sock$base$id$ext.pid";
                my $pid = processexists($f);
                if($pid > 0) {
                    printf ("* kill pid for %s => %d\n", "ftp-$base$id$ext",
                        $pid) if($verbose);
                    $pidlist .= "$pid ";
                }
                push @pidfiles, $f;
            }
        }
    }

    killpid($verbose, $pidlist);

    foreach my $pidfile (@pidfiles) {
        unlink($pidfile);
    }
}


sub set_advisor_read_lock {
    my ($filename) = @_;

    if(open(FILEH, ">$filename")) {
        close(FILEH);
        return;
    }
    printf "Error creating lock file $filename error: $!";
}


sub clear_advisor_read_lock {
    my ($filename) = @_;

    if(-f $filename) {
        unlink($filename);
    }
}


1;
