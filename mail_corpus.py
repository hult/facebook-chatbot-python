import sys
import mailbox
import mail_parser

def main():
    """Extract the texts of emails from a specified mailbox and
    from a specified set of senders and write corpus.txt.

    Usage: python mail_corpus.py mboxfile email1@example.com email2@example.com
    """
    mbox = mailbox.mbox(sys.argv[1])
    addresses = set(sys.argv[2:])
    f = open("corpus.txt", "w")
    for text in mail_parser.mail_texts(mbox, addresses):
        print >> f, text
    f.close()

if __name__ == '__main__':
    main()
