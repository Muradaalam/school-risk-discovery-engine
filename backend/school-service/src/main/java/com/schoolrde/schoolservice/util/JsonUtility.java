package com.schoolrde.schoolservice.util;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

public class JsonUtility{
    
	private static final ObjectMapper objectMapper = new ObjectMapper();

    public static String toJson(Object object){
        try{
            return objectMapper.writeValueAsString(object);
        }catch (JsonProcessingException ex) {
            throw new IllegalArgumentException("Error : Failed to convert object to JSON", ex);
        }
    }

    public static JsonNode toObject(String json) {
        try{
            return objectMapper.readTree(json);
        }catch (JsonProcessingException ex) {
            throw new IllegalArgumentException("Error : Failed to convert JSON to object", ex);
        }
    }
}