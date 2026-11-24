package com.schoolrde.schoolservice.dto;

public class RequestLoggerDto{
    private String api;
    private String method;
    private String requestBody;

    // Getters and setters are generated using STS: Source > Generate Getters and Setters
   public String getApi(){
        return api;
    }

    public void setApi(String api){
        this.api=api;
    }

    public String getMethod(){
        return method;
    }

    public void setMethod(String method){
        this.method=method;
    }

    public String getRequestBody(){
        return requestBody;
    }

    public void setRequestBody(String requestBody){
        this.requestBody=requestBody;
    }
}
