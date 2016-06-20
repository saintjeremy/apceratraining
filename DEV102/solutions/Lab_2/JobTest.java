import java.net.*;
import java.io.*;

public class JobTest 
{ 
  public static void main(String[] args) 
  {
    String urlStr = "http://api.kiso.io/v1/jobs";

    try {

        URL url = new URL(urlStr);

        HttpURLConnection conn =
        (HttpURLConnection) url.openConnection();

        String token = "eyJ0eXAiOiIiLCJhbGciOiIifQ.eyJpc3MiOiJhdXRoX3NlcnZlckBhcGNlcmEubWUiLCJhdWQiOiJhcGNlcmEubWUiLCJpYXQiOjE0NjQzMDc4NTgsImV4cCI6MTQ2NDM5NDI2OCwicHJuIjoieW9rby5oeWFrdW5hQGFwY2VyYS5jb20iLCJjbGFpbXMiOlt7Iklzc3VlciI6ImF1dGhfc2VydmVyQGFwY2VyYS5tZSIsIlR5cGUiOiJhdXRoVHlwZSIsIlZhbHVlIjoiZ29vZ2xlVXNlckluZm8ifV19.MEYCIQCPKOUqjtYkQguPeh_xylfMYlDBIPQRutPlxh_x9uaPFgIhAPHfQoZ6k4DIKd4DGX9bRGFkbkLjns3_cJV0IWfFY9cX";

        conn.setRequestProperty("Content-Type", "application/json");
        conn.setRequestProperty("Authorization", "Bearer " + token);
        conn.setRequestMethod("GET");

        if (conn.getResponseCode() != 200) {
          System.out.println("Connection failed");
        }

        // Buffer the result into a string
        BufferedReader rd = new BufferedReader(
            new InputStreamReader(conn.getInputStream()));

        StringBuilder sb = new StringBuilder();

        String line;
        while ((line = rd.readLine()) != null) {
          sb.append(line);
        }
        rd.close();

        conn.disconnect();
        
        System.out.println(sb.toString());
    }
    catch (IOException ex)
    {
      System.out.println(ex.toString());
    }
    catch (Exception e)
    {
      System.out.println(e.toString());
    }
  }
}
