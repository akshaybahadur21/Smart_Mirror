#include "speex/speex.h"
#include "speex/speex_header.h"
#ifdef _WIN32
    #include <winsock2.h>
    #pragma comment(lib, "Ws2_32.lib")
#else
    #include <arpa/inet.h>      /* htons */
#endif
#include <string.h>

static struct {
    SpeexBits bits;
    void *enc_state;
} SH_speex;

int SH_speex_init(int quality, char *buffer, int isNB, int buflen)
{
    int q = quality;
	SpeexHeader speex_header;
	int packet_size;
	char *packet;
    
	if (!isNB)
        SH_speex.enc_state = speex_encoder_init(&speex_wb_mode);
    else
        SH_speex.enc_state = speex_encoder_init(&speex_nb_mode);
	
    speex_encoder_ctl(SH_speex.enc_state, SPEEX_SET_QUALITY, &q);
    speex_bits_init(&SH_speex.bits);

    if (!isNB)
        speex_init_header(&speex_header, 16000, 1, &speex_wb_mode);
    else
        speex_init_header(&speex_header, 8000, 1, &speex_nb_mode);
    
    packet = speex_header_to_packet(&speex_header, &packet_size);
    memcpy(buffer, packet, (buflen < packet_size) ? buflen : packet_size);

    return packet_size;
}


// Reads audio samples (20ms, 16 bit unsigned ints)
// Writes into cbits (must be at least 202 bytes)
int SH_speex_encode_frame(short *sFrame, char *cbits)
{
	int nbytes;
	unsigned short nbytes_s;
	
    speex_bits_reset(&SH_speex.bits);
    speex_encode_int(SH_speex.enc_state, sFrame, &SH_speex.bits);

    nbytes = speex_bits_write(&SH_speex.bits, cbits + 2, 200);
    nbytes_s = (unsigned short)nbytes;
    nbytes_s = htons(nbytes_s);
    *((unsigned short *)cbits) = nbytes_s;

    return nbytes;
}
