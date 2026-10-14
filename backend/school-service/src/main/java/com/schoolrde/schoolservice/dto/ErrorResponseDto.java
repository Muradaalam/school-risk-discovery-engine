package com.schoolrde.schoolservice.dto;

public class ErrorResponseDto{
    private String errorCode;
    private String errorDescription;

    public ErrorResponseDto(String errorCode,String errorDescription){
        this.errorCode=errorCode;
        this.errorDescription=errorDescription;
    }

    public String getErrorCode(){
    	return errorCode;
    }
    public String getErrorDescription(){
    	return errorDescription;
    }
}