/**
* @author: Ashish Gaikwad <ash.gkwd@gmail.com>
* @description: simple Java client for ag-chat server.
**/

import java.net.*;
import java.io.*;
import java.util.*;

public class ClientAgChat
{
 public static void main(String [] args)
 {
  String address = args[0];
  int port = Integer.parseInt(args[1]);

  try
  {
    System.out.println("Connecting to " + address + " on port " + port);
    Socket client = new Socket(address, port);

    DataOutputStream out = new DataOutputStream(client.getOutputStream());

    out.writeUTF("\r\n.Hello from " + client.getLocalSocketAddress() + ".\r\n");

    Thread userInputThread = new Thread(new Runnable() {
      DataOutputStream dos;
      Socket client;

      private Runnable init(DataOutputStream d, Socket c) {
        System.out.println("Initializing Runnable");
        dos = d;
        client = c;
        return this;
      }

      public void run () {
        Scanner sc = new Scanner(System.in);
        sc.useDelimiter("\n");
        while (true) {
          System.out.print("_> ");
          String i = sc.next();

          try {
            dos.flush();
            if (i.equals("exit")) {
              client.close();
              System.exit(0);
            }
            dos.writeBytes(i + "\r\n");
          } catch(IOException e) {
            System.out.println("userInputThread got IOException");
            e.printStackTrace();
          }
        }
      }
    }.init(out, client));

    userInputThread.start();

    BufferedReader in = new BufferedReader(new InputStreamReader(client.getInputStream()));
    while (true) {
      System.out.println("" + in.readLine());
    }
  } catch(IOException e) {
   e.printStackTrace();
 }
}
}
