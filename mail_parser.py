import sys
from email_reply_parser import EmailReplyParser

def mail_texts(mailbox, from_addresses=None):
    """Generate email texts from the specified mailbox. If
    from_addresses is a set of email addresses, only generate texts
    from those emails.

    This function tries to extract only the part written by the
    email's author, not the stuff they're replying to and not the
    signatures.
    """
    for message in mailbox:
        if from_addresses is None or message['from'] in from_addresses:
            if message.is_multipart():
                # Find a text/plain part
                for part in message.walk():
                    if part.get_content_type() == 'text/plain':
                        text = part.get_payload(decode=True)
                        break
            else:
                text = message.get_payload(decode=True)

            reply = EmailReplyParser.parse_reply(text)
            reply = reply.strip()

            # Ugly hack: exclude OTR encrpyted messages
            if '?OTR' in reply[:50]:
                print >> sys.stderr, "Excluding OTR message"
                print >> sys.stderr, reply[:50]
                continue

            # Ugly hack: some chat messages are duplicated
            # ("hi bobhi bob"). Fix them.
            if len(reply) > 10 and len(reply) % 2 == 0:
                half = len(reply) / 2
                if reply[:half] == reply[half:]:
                    print >> sys.stderr, "Fixing duplicated message"
                    print >> sys.stderr, reply
                    reply = reply[:half]

            yield reply

if __name__ == '__main__':
    main()
