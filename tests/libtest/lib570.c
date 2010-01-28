/*****************************************************************************
 *                                  _   _ ____  _
 *  Project                     ___| | | |  _ \| |
 *                             / __| | | | |_) | |
 *                            | (__| |_| |  _ <| |___
 *                             \___|\___/|_| \_\_____|
 *
 * $Id: lib570.c,v 1.1 2010-01-28 04:58:04 yangtse Exp $
 */

#include "test.h"

#include <curl/mprintf.h>

#include "memdebug.h"

/* build request url */
static char *suburl(const char *base, int i)
{
  return curl_maprintf("%s%.4d", base, i);
}

int test(char *URL)
{
  CURLcode res;
  CURL *curl;
  int request=1;
  char *stream_uri;

  if (curl_global_init(CURL_GLOBAL_ALL) != CURLE_OK) {
    fprintf(stderr, "curl_global_init() failed\n");
    return TEST_ERR_MAJOR_BAD;
  }

  if ((curl = curl_easy_init()) == NULL) {
    fprintf(stderr, "curl_easy_init() failed\n");
    curl_global_cleanup();
    return TEST_ERR_MAJOR_BAD;
  }

  curl_easy_setopt(curl, CURLOPT_HEADERDATA, stdout);
  curl_easy_setopt(curl, CURLOPT_WRITEDATA, stdout);
  curl_easy_setopt(curl, CURLOPT_VERBOSE, 1L);

  curl_easy_setopt(curl, CURLOPT_URL, URL);

  curl_easy_setopt(curl, CURLOPT_RTSP_REQUEST, CURL_RTSPREQ_OPTIONS);

  stream_uri = suburl(URL, request++);
  curl_easy_setopt(curl, CURLOPT_RTSP_STREAM_URI,stream_uri);
  free(stream_uri);

  res = curl_easy_perform(curl);
  if(res != CURLE_RTSP_CSEQ_ERROR) {
    fprintf(stderr, "Failed to detect CSeq mismatch");
    return res;
  }

  curl_easy_setopt(curl, CURLOPT_RTSP_CLIENT_CSEQ, 999);
  curl_easy_setopt(curl, CURLOPT_RTSP_TRANSPORT,
                         "RAW/RAW/UDP;unicast;client_port=3056-3057");
  curl_easy_setopt(curl, CURLOPT_RTSP_REQUEST, CURL_RTSPREQ_SETUP);

  stream_uri = suburl(URL, request++);
  curl_easy_setopt(curl, CURLOPT_RTSP_STREAM_URI,stream_uri);
  free(stream_uri);

  res = curl_easy_perform(curl);
  if(res)
    return res;

  curl_easy_setopt(curl, CURLOPT_RTSP_REQUEST, CURL_RTSPREQ_PLAY);
  stream_uri = suburl(URL, request++);
  curl_easy_setopt(curl, CURLOPT_RTSP_STREAM_URI,stream_uri);
  free(stream_uri);

  res = curl_easy_perform(curl);
  if(res != CURLE_RTSP_SESSION_ERROR) {
    fprintf(stderr, "Failed to detect a Session ID mismatch");
  }

  curl_easy_cleanup(curl);
  curl_global_cleanup();

  return (int)res;
}

