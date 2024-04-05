package io.confluent.developer;

import io.confluent.ksql.function.udf.Udf;
import io.confluent.ksql.function.udf.UdfDescription;
import io.confluent.ksql.function.udf.UdfParameter;

import okhttp3.*;
import java.io.IOException;
import java.util.HashMap;
import org.json.JSONObject;

@UdfDescription(name = "sentiment", description = "Sentiment of user")
public class SentimentUdf {

    @Udf(description = "sentiment for text as String, returns HashMap")
    public HashMap<String, Object> sentiment(
            @UdfParameter(value = "text")
            final String text) {
        OkHttpClient client = new OkHttpClient();
        String url = "https://sentiment-analysis-api-production-13e3.up.railway.app/api/v1/sentiment/text=" + text;
        Request request = new Request.Builder()
                .url(url)
                .build();
        try {
            Response response = client.newCall(request).execute();
            if (!response.isSuccessful()) {
                throw new IOException("Unexpected code " + response);
            }
            // Parse response JSON
            String responseBody = response.body().string();
            JSONObject json = new JSONObject(responseBody);

            // Extract sentiment analysis data
            JSONObject sentimentJson = json.getJSONObject("sentiment");
            String label = sentimentJson.getString("label");
            double score = sentimentJson.getDouble("score");

            // Create HashMap to store sentiment data
            HashMap<String, Object> sentimentData = new HashMap<>();
            sentimentData.put("label", label);
            sentimentData.put("score", score);

            return sentimentData;
        } catch (IOException e) {
            e.printStackTrace(); // Or handle the exception appropriately
            return null; // Return null or throw a custom exception
        }
    }
}