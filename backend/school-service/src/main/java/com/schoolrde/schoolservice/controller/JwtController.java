package com.schoolrde.schoolservice.controller;
//JwtController has been implemented with AI assistance 


import java.util.Map;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import com.schoolrde.schoolservice.dto.RequestLoggerDto;
import com.schoolrde.schoolservice.dto.ResponseLoggerDto;
import com.schoolrde.schoolservice.service.JwtService;
import com.schoolrde.schoolservice.util.JsonUtility;

import jakarta.servlet.http.HttpServletRequest;

@RestController
@RequestMapping("${spring.application.name}/auth")
public class JwtController{

    private static final Logger LOGGER = LoggerFactory.getLogger(JwtController.class);

    private final JwtService jwtService;

    @Value("${api.username}")
    private String apiUsername;

    @Value("${api.password}")
    private String apiPassword;
    
    @Value("${jwt.expiration}")
    private int jwtExpiration;
    
    public JwtController(JwtService jwtService){
        this.jwtService = jwtService;
    }

    @PostMapping("/generateToken")
    public ResponseEntity<?> generateToken(@RequestBody Map<String, String> requestDto, HttpServletRequest request) throws Exception{

        String uri = request.getRequestURI();
        String method = request.getMethod();

        RequestLoggerDto requestLoggerDto = new RequestLoggerDto();
        requestLoggerDto.setApi(uri);
        requestLoggerDto.setMethod(method);

        requestLoggerDto.setRequestBody("{\"username\":\"" + requestDto.get("username") + "\"}");

        LOGGER.info("Request: {}", JsonUtility.toJson(requestLoggerDto));

        String username = requestDto.get("username");
        String password = requestDto.get("password");

        if (username == null || password == null || !apiUsername.equals(username) || !apiPassword.equals(password)){

            ResponseLoggerDto responseLoggerDto = new ResponseLoggerDto();
            responseLoggerDto.setApi(uri);
            responseLoggerDto.setMethod(method);
            responseLoggerDto.setStatusCode(HttpStatus.UNAUTHORIZED.value());
            responseLoggerDto.setResponseBody("Invalid username or password");

            LOGGER.info("Response: {}", JsonUtility.toJson(responseLoggerDto));

            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body("Invalid username or password");
        }

        String token = jwtService.generateToken(username);

        Map<String, Object> responseDto = Map.of("token", token, "tokenType", "Bearer", "expiresIn", jwtExpiration / 1000);

        ResponseLoggerDto responseLoggerDto = new ResponseLoggerDto();
        responseLoggerDto.setApi(uri);
        responseLoggerDto.setMethod(method);
        responseLoggerDto.setStatusCode(HttpStatus.OK.value());
        responseLoggerDto.setResponseBody(JsonUtility.toJson(responseDto));

        LOGGER.info("Response: {}", JsonUtility.toJson(responseLoggerDto));

        return ResponseEntity.ok(responseDto);
    }
}
