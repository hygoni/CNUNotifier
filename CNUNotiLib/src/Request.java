import java.io.BufferedInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;

import org.apache.commons.io.IOUtils;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

public class Request {
	
	public JSONObject getNew (String urlString, String departName, int lastArticle) {

		JSONObject request = new JSONObject();
		JSONObject response = null;
		request.put("departName", departName);
		request.put("lastArticle", lastArticle);
		
		try {
			
			URL url = new URL(urlString);
			HttpURLConnection conn = (HttpURLConnection) url.openConnection();
			
			conn.setRequestMethod("POST");
			conn.setRequestProperty("Content-Type", "application/json; utf-8"); //Request format
			conn.setRequestProperty("Accept", "application/json"); //Response format
			conn.setDoOutput(true);
			conn.setDoInput(true);
			OutputStream  os = conn.getOutputStream();
			os.write(request.toJSONString().getBytes("UTF-8"));
			os.close();
			
			InputStream in = new BufferedInputStream(conn.getInputStream());
			String result = IOUtils.toString(in, "UTF-8");
			response = (JSONObject) new JSONParser().parse(result);
			
		} catch (MalformedURLException e) {
			e.printStackTrace();
		} catch(IOException e) {
			e.printStackTrace();
		} catch(ParseException e) {
			e.printStackTrace();
		}
		
		return response;
	}
		
		
		
	

}
