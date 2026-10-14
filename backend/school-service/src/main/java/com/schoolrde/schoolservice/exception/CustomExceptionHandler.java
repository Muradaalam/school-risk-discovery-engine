package com.schoolrde.schoolservice.exception;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.context.annotation.PropertySource;
import org.springframework.core.env.Environment;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

import com.schoolrde.schoolservice.dto.ErrorResponseDto;

@PropertySource("classpath:error.properties")
@RestControllerAdvice
public class CustomExceptionHandler{
    private final Environment environment;
    private final ObjectMapper objectMapper;

    private static final Logger LOGGER = LoggerFactory.getLogger(CustomExceptionHandler.class);

    private static final String INTERNAL_SERVER_ERROR_CODE = "E9999";
    private static final String INTERNAL_SERVER_ERROR_MSG = "Internal Server Error";


    public CustomExceptionHandler(Environment environment,ObjectMapper objectMapper){
        this.environment=environment;
        this.objectMapper=objectMapper;
    }

    @org.springframework.web.bind.annotation.ExceptionHandler(CustomException.class)
    public ResponseEntity<ErrorResponseDto> handleCustomException(CustomException ex){
        String errorCode=ex.getErrorCode();
        String errorProperty=environment.getProperty(errorCode);

        try{
            JsonNode error=objectMapper.readTree(errorProperty);
            String message=ex.getCustomMessage();

            if(message==null){
                message=error.get("errorDescription").asText();
            }

            int code=error.get("httpCode").asInt();
            HttpStatus status=HttpStatus.valueOf(code);

            ErrorResponseDto response=new ErrorResponseDto(errorCode,message);

            return new ResponseEntity<>(response,status);
        }catch(Exception exp){
        	LOGGER.error("Error : Unable to process error code: {}", errorCode, exp);
            ErrorResponseDto response=new ErrorResponseDto(INTERNAL_SERVER_ERROR_CODE,INTERNAL_SERVER_ERROR_MSG);
            return new ResponseEntity<>(response,HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponseDto> handleException(Exception ex){
    	LOGGER.error("Error : Unexpected exception occurred", ex);
        ErrorResponseDto response=new ErrorResponseDto(INTERNAL_SERVER_ERROR_CODE,INTERNAL_SERVER_ERROR_MSG);
        return new ResponseEntity<>(response,HttpStatus.INTERNAL_SERVER_ERROR);
    }
}