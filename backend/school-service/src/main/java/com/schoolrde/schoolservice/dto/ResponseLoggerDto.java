package com.schoolrde.schoolservice.dto;

public class ResponseLoggerDto{
    private String api;
    private String method;
    private int statusCode;
    private String responseBody;

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

    public int getStatusCode(){
        return statusCode;
    }

    public void setStatusCode(int statusCode){
        this.statusCode=statusCode;
    }

    public String getResponseBody(){
        return responseBody;
    }

    public void setResponseBody(String responseBody){
        this.responseBody=responseBody;
    }
}
