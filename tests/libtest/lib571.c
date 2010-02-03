/*****************************************************************************
 *                                  _   _ ____  _
 *  Project                     ___| | | |  _ \| |
 *                             / __| | | | |_) | |
 *                            | (__| |_| |  _ <| |___
 *                             \___|\___/|_| \_\_____|
 *
 * $Id: lib571.c,v 1.5 2010-02-03 06:49:27 yangtse Exp $
 */

#include "test.h"

#ifdef HAVE_SYS_SOCKET_H
#  include <sys/socket.h>
#endif
#ifdef HAVE_NETINET_IN_H
#  include <netinet/in.h>
#endif
#ifdef HAVE_NETDB_H
#  include <netdb.h>
#endif
#ifdef HAVE_ARPA_INET_H
#  include <arpa/inet.h>
#endif
#ifdef HAVE_SYS_STAT_H
#  include <sys/stat.h>
#endif
#ifdef HAVE_FCNTL_H
#  include <fcntl.h>
#endif

#include <curl/mprintf.h>

#include "memdebug.h"

#define RTP_PKT_CHANNEL(p)   ((int)((unsigned char)((p)[1])))

#define RTP_PKT_LENGTH(p)  ((((int)((unsigned char)((p)[2]))) << 8) | \
                             ((int)((unsigned char)((p)[3]))))

#define RTP_DATA_SIZE 12
static const char *RTP_DATA = "$_1234\n\0asdf";

static int rtp_packet_count = 0;

static size_t rtp_write(void *ptr, size_t size, size_t nmemb, void *stream) {
  char *data = (char *)ptr;
  int channel = RTP_PKT_CHANNEL(data);
  int message_size = (int)(size * nmemb) - 4;
  int coded_size = RTP_PKT_LENGTH(data);
  size_t failure = (size * nmemb) ? 0 : 1;
  int i;
  (void)stream;

  printf("RTP: message size %d, channel %d\n", message_size, channel);
  if(message_size != coded_size) {
    printf("RTP embedded size (%d) does not match the write size (%d).\n",
           coded_size, message_size);
    return failure;
  }

  data += 4;
  for(i = 0; i < message_size; i+= RTP_DATA_SIZE) {
    if(message_size - i > RTP_DATA_SIZE) {
      if(memcmp(RTP_DATA, data + i, RTP_DATA_SIZE) != 0) {
        printf("RTP PAYLOAD CORRUPTED [%s]\n", data + i);
        return failure;
      }
    } else {
      if (memcmp(RTP_DATA, data + i, message_size - i) != 0) {
        printf("RTP PAYLOAD END CORRUPTED (%d), [%s]\n",
               message_size - i, data + i);
        return failure;
      }
    }
  }

  rtp_packet_count++;
  fprintf(stderr, "packet count is %d\n", rtp_packet_count);

  return size * nmemb;
}

/* build request url */
static char *suburl(const char *base, int i)
{
  return curl_maprintf("%s%.4d", base, i);
}

int test(char *URL)
{
  CURLcode res;
  CURL *curl;
  char *stream_uri;
  int request=1;
  FILE *protofile;

  protofile = fopen(libtest_arg2, "wb");
  if(protofile == NULL) {
    fprintf(stderr, "Couldn't open the protocol dump file\n");
    return TEST_ERR_MAJOR_BAD;
  }

  if (curl_global_init(CURL_GLOBAL_ALL) != CURLE_OK) {
    fprintf(stderr, "curl_global_init() failed\n");
    fclose(protofile);
    return TEST_ERR_MAJOR_BAD;
  }

  if ((curl = curl_easy_init()) == NULL) {
    fprintf(stderr, "curl_easy_init() failed\n");
    curl_global_cleanup();
    fclose(protofile);
    return TEST_ERR_MAJOR_BAD;
  }
  curl_easy_setopt(curl, CURLOPT_URL, URL);

  stream_uri = suburl(URL, request++);
  curl_easy_setopt(curl, CURLOPT_RTSP_STREAM_URI,stream_uri);
  free(stream_uri);

  curl_easy_setopt(curl, CURLOPT_INTERLEAVEFUNCTION, rtp_write);
  curl_easy_setopt(curl, CURLOPT_TIMEOUT, 3);
  curl_easy_setopt(curl, CURLOPT_VERBOSE, 1L);
  curl_easy_setopt(curl, CURLOPT_WRITEDATA, protofile);

  curl_easy_setopt(curl, CURLOPT_RTSP_TRANSPORT, "RTP/AVP/TCP;interleaved=0-1");
  curl_easy_setopt(curl, CURLOPT_RTSP_REQUEST, CURL_RTSPREQ_SETUP);
  res = curl_easy_perform(curl);

  /* This PLAY starts the interleave */
  stream_uri = suburl(URL, request++);
  curl_easy_setopt(curl, CURLOPT_RTSP_STREAM_URI,stream_uri);
  free(stream_uri);
  curl_easy_setopt(curl, CURLOPT_RTSP_REQUEST, CURL_RTSPREQ_PLAY);
  res = curl_easy_perform(curl);

  /* The DESCRIBE request will try to consume data after the Content */
  stream_uri = suburl(URL, request++);
  curl_easy_setopt(curl, CURLOPT_RTSP_STREAM_URI,stream_uri);
  free(stream_uri);
  curl_easy_setopt(curl, CURLOPT_RTSP_REQUEST, CURL_RTSPREQ_DESCRIBE);

  res = curl_easy_perform(curl);

  stream_uri = suburl(URL, request++);
  curl_easy_setopt(curl, CURLOPT_RTSP_STREAM_URI,stream_uri);
  free(stream_uri);
  curl_easy_setopt(curl, CURLOPT_RTSP_REQUEST, CURL_RTSPREQ_PLAY);
  res = curl_easy_perform(curl);

  fprintf(stderr, "PLAY COMPLETE\n");

  /* Use Receive to get the rest of the data */
  while(!res && rtp_packet_count < 13) {
    fprintf(stderr, "LOOPY LOOP!\n");
    curl_easy_setopt(curl, CURLOPT_RTSP_REQUEST, CURL_RTSPREQ_RECEIVE);
    res = curl_easy_perform(curl);
  }

  curl_easy_cleanup(curl);
  curl_global_cleanup();
  fclose(protofile);

  return (int)res;
}

