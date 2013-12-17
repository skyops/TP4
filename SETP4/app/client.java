/*  The java.net package contains the basics needed for network operations. */
import java.net.*;
import java.io.IOException;
import java.io.FileReader;
import java.io.BufferedReader;
/* The java.io package contains the basics needed for IO operations. */
import java.io.*;
/** The SocketClient class is a simple example of a TCP/IP Socket Client.
 *
 */
import xml.dom.minidom
public class SocketClient 
{
	
	//On compare la longitude et latitude de l'utilisateur avec ceux dans le fichier contenant 
	//les coordonées des réseaux et on affiche celui dont les coordonées sont les plus semblables à 
	//ceux de lutilisateur
	public void AfficherWifiPlusProche(string longitude, string latitude)
	{
		
	}
	
	public class TelechargerTXT{
        public static void main(String[] args) throws IOException{

        		string  requeteXML = "<telechargerFichier>" + \"</telechargerFichier>"
        	
                FileOutputStream fileOutputStream =new  FileOutputStream("sampleFile.txt");
                BufferedOutputStream bufferedOutputStream = new BufferedOutputStream(fileOutputStream, 1024);

                byte data[] = new byte[1024];
                while(bufferedInputStream.read(data, 0, 1024) >=0 )
                {
                        bufferedOutputStream.write(data);
                }

                bufferedOutputStream.close();
                bufferedInputStream.close();
        }                               
}
	
	public ArrayList<String> ListeReseaux(string pathFichier)
	
	{
		 BufferedReader in = new BufferedReader(new FileReader(pathFichier));
		 String str=null;
		 ArrayList<String> lines = new ArrayList<String>();
		 while((str = in.readLine()) != null){
		        lines.add(str);
		    }
		 String[] linesArray = lines.toArray(new String[lines.size());
		 
		 return linesArray;
	}
	
	public static void main(String[] args) {
	    /** Define a host server */
	    String host = "localhost";
	    /** Define a port */
	    int port = 19999;

	    StringBuffer instr = new StringBuffer();
	    String TimeStamp;
	    System.out.println("SocketClient initialized");
	    
	    try 
	    {
	        /** Obtain an address object of the server */
	        InetAddress address = InetAddress.getByName(host);
	        /** Establish a socket connetion */
	        Socket connection = new Socket(address, port);
	        /** Instantiate a BufferedOutputStream object */
	        BufferedOutputStream bos = new BufferedOutputStream(connection.
	                getOutputStream());

	        /** Instantiate an OutputStreamWriter object with the optional character
	        * encoding.
	        */
	        OutputStreamWriter osw = new OutputStreamWriter(bos, "US-ASCII");
	        TimeStamp = new java.util.Date().toString();
	        String process = "Calling the Socket Server on "+ host + " port " + port +
	            " at " + TimeStamp +  (char) 13;

	        /** Write across the socket connection and flush the buffer */
	        osw.write(process);
	        osw.flush();
	        /** Instantiate a BufferedInputStream object for reading
	        /** Instantiate a BufferedInputStream object for reading
	         * incoming socket streams.
	         */

	        BufferedInputStream bis = new BufferedInputStream(connection.
	            getInputStream());
	        /**Instantiate an InputStreamReader with the optional
	         * character encoding.
	         */

	        InputStreamReader isr = new InputStreamReader(bis, "US-ASCII");

	        /**Read the socket's InputStream and append to a StringBuffer */
	        int c;
	        while ( (c = isr.read()) != 13)
	          instr.append( (char) c);

	        /** Close the socket connection. */
	        connection.close();
	        System.out.println(instr);
	       }
	      catch (IOException f) {
	        System.out.println("IOException: " + f);
	      }
	      catch (Exception g) {
	        System.out.println("Exception: " + g);
	      }
	    }
	  }
}