# Custom go/ links

Custom go/ links that are setup through a simple python HTTPs server with configurations with Alfred!

Inspired by [golinks](https://golinks.io/) and [go-alfred](https://github.com/kswilster/go-alfred)

## Setup

### Generate a new certificate

Required to serve our https server, store in same directory as the repository

```bash
openssl req -new -x509 -keyout server.pem -out server.pem -days 365 -nodes
```

### Setup `mapping.json` file

This is your database file with the following format:
```json
{
    "shortlink": "https://example.com"
}
```

There is a `mapping.json.template` file in the repository that you can rename to `mapping.json` to get started

### Setup Alfred workflow

Import the [setup/go.alfredworkflow](setup/go.alfredworkflow) package into alfred, you will need to purchase the powerpack

### Setup `/etc/hosts` file

To setup `https://go/` to work for you you will need to add a loopback from your local IP address to the go domain, which can be done by adding the line below to your `/etc/hosts` file

```
127.0.0.1 go
```

### Start server

**Notes**:
- The server binds to port 443 (`https`) and listens for requests, and thus needs to be started with `sudo`
- The `&` at the end is to start the server in the background
- The `--goserver` argument adds as an easy way to search for the process using `ps -a | grep goserver` for when you actually want to kill it (you will need to use `sudo kill <pid>` to actually kill the process)
- The automatic start workflow using `launchd` is documented at the bottom as an optional alternative to starting the server manually

```bash
sudo python3 main.py --goserver &
```



## How to Use

### Alfred

#### Create a new shortlink

If `test` is your short keyword, and `https://example.com` is your destination link then you can setup the mapping by going into alfred and typing `new` and then `test` which is your shortlink and then your domain `https://example.com` and then pressing enter, it will automatically navigate you to the URL below [https://go/new?test=https://example.com](https://go/new?test=https://example.com), and the resulting webpage should confirm that the mapping has been added

![Create a new link](https://media4.giphy.com/media/GRLffwcRlCJcNHq4dp/giphy.gif?cid=790b761162c7338f0ff4af917877b80d22d35155a089851b&rid=giphy.gif&ct=g)


#### Open a shortlink

To open a shortlink that you have created eg: `test` from above, all you have to do is open alfred type `go` and then `test` which is your shortlink and then pressing enter and the browser should open the destination link

![Open a shortlink](https://media0.giphy.com/media/eTUTJqQQbjPgebgzY2/giphy.gif?cid=790b7611455a4ad0b712306dd9bd00d5d3feef60fd6f4c28&rid=giphy.gif&ct=g)


#### Delete a shortlink

If `test` is your short keyword, you can delete the mapping by going into alfred and typing `delete` and then `test` which is your shortlink and then pressing enter, it will automatically navigate you to the URL below [https://go/delete?test=delete](https://go/delete?test=delete) and the resulting webpage should confirm that the mapping has been deleted

![Delete a shortlink](https://media3.giphy.com/media/1ixAZ6ZQ3KKqC5dcO9/giphy.gif?cid=790b7611f5144624c939ccf4da6e3670d0626506580cab26&rid=giphy.gif&ct=g)



### Browser

#### Create a new shortlink

If `test` is your short keyword, and `https://example.com` is your destination link then you can setup the mapping by navigating to [https://go/new?test=https://example.com](https://go/new?test=https://example.com) and the resulting webpage should confirm that the mapping has been added


#### Open a shortlink

If you are trying to open a shortlink that you have created eg: `test` from above, all you have to do is navigate to `https://go/test` and the browser will open the destination link


## Useful Notes

1. There is a metrics logging file `metrics.csv` that logs the visit time of each shortlink with its corresponding destination domain (Refer `metrics.csv.template` for format example)
2. You can configure the port, the mapping file, the metrics file, the prefix to create a new domain, as well as the path of the certificate file all through the `config.ini` file
3. This service can also be setup as a `launchd` service using the [setup/com.adityaarora.golinks.plist](setup/com.adityaarora.golinks.plist) file as reference. Ensure you change the `WorkingDirectory` as well as the `StandardOutPath` and `StandardErrorPath`. After that simply store the file in `/Library/LaunchDaemons` and then run `sudo launchctl load /Library/LaunchDaemons/com.adityaarora.golinks.plist` to load the service. The service should  be started automatically, and if there are any issues you can inspect the log files you put in.