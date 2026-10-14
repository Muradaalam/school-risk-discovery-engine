package com.schoolrde.schoolservice.exception;


public final class CustomException extends RuntimeException {


	private final String errorCode;
    private String message;

    public CustomException(final String errorCode){
    	super(errorCode);
    	this.errorCode=errorCode;
    }

    public CustomException(final String errorCode, final String message) {
    	super(errorCode);
    	this.errorCode=errorCode;
    	this.message = message;
    }
    
    public String getErrorCode(){
    	return errorCode;
    }

    public String getCustomMessage(){
    	return message;
    }
}
