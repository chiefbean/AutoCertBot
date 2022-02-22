import jinja2
import sys
import os

def main(args):
    if not os.geteuid() == 0:
        sys.exit('Please run this with sudo or there will be a lot of clean up')
    env = jinja2.Environment(loader=jinja2.FileSystemLoader('./'))
    try:
        conf = env.get_template('nginx-config.template')
    except jinja2.TemplateNotFound as err:
        print("The template does not exist")
        return
    
    domain = args[1]

    if not (os.path.exists("/etc/letsencrypt/live/%s/fullchain.pem" % domain) and os.path.exists("/etc/letsencrypt/live/%s/privkey.pem" % domain)):
        print('[*] Generating certs.')
        if os.system("certbot certonly --nginx -d %s" % domain) != 0:
            print('[*] Error generating certs, please try again.')
            exit(1)
    else:
        print("[+] Certs already exist. Skipping.")

    if not (os.path.exists("/etc/nginx/sites-available/%s.conf" % domain)):
        print("[*] Generating config.")
        with open('/etc/nginx/sites-available/%s.conf' % domain, 'wb') as f:
            config_add = conf.render(domain=domain)
            f.write(config_add.encode('utf-8'))
            f.close()
    else:
        print("[+] Config already exists. Skipping.")

    if not (os.path.exists("/etc/nginx/sites-enabled/%s.conf" % domain)):
        print("[*] Enabling config.")
        os.system("ln -s /etc/nginx/sites-available/%s.conf /etc/nginx/sites-enabled/%s.conf" % (domain, domain))
    else:
        print("[+] Config already enabled")

    print("[*] Restarting webserver.")
    os.system("service nginx restart")
    print("[*] Webserver restarted.")


if __name__ == '__main__':
    main(sys.argv)

