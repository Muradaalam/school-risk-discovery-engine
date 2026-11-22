package com.schoolrde.schoolservice.config;
//JwtAuthenticationFilter file is implemented with AI assistance 

import java.io.IOException;
import java.util.Collections;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.context.annotation.PropertySource;
import org.springframework.core.env.Environment;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import com.fasterxml.jackson.databind.JsonNode;
import com.schoolrde.schoolservice.dto.ErrorResponseDto;
import com.schoolrde.schoolservice.service.JwtService;
import com.schoolrde.schoolservice.util.JsonUtility;

import io.jsonwebtoken.ExpiredJwtException;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

@Component
@PropertySource("classpath:error.properties")
public class JwtAuthenticationFilter extends OncePerRequestFilter{

	 private static final Logger LOGGER = LoggerFactory.getLogger(JwtAuthenticationFilter.class);

	 private final JwtService jwtService;
	 private final Environment environment;

	 public JwtAuthenticationFilter(JwtService jwtService, Environment environment){
	     this.jwtService = jwtService;
	     this.environment = environment;
	 }


	 @Override
	 protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain) throws ServletException, IOException{

	     String authHeader = request.getHeader("Authorization");

	     if(authHeader == null || !authHeader.startsWith("Bearer ")){
	         filterChain.doFilter(request, response);
	         return;
	     }

	     String token = authHeader.substring(7);

	     try{

	         if(!jwtService.validateToken(token)){

	             LOGGER.warn("Invalid JWT token");

	             sendErrorResponse(response, "E9101");
	             return;
	         }

	         String username = jwtService.extractUsername(token);

	         UsernamePasswordAuthenticationToken authentication = new UsernamePasswordAuthenticationToken(
	                 username, null, Collections.emptyList());

	         SecurityContextHolder.getContext().setAuthentication(authentication);

	     }catch(ExpiredJwtException ex){

	         LOGGER.warn("JWT token is expired");

	         SecurityContextHolder.clearContext();

	         sendErrorResponse(response, "E9102");
	         return;

	     }catch(Exception ex){

	         LOGGER.warn("JWT authentication failed : {}", ex.getMessage());

	         SecurityContextHolder.clearContext();

	         sendErrorResponse(response, "E9011");
	         return;
	     }

	     filterChain.doFilter(request, response);
	 }


	 private void sendErrorResponse(HttpServletResponse response, String errorCode) throws IOException{

	     String errorProperty = environment.getProperty(errorCode);

	     JsonNode error = JsonUtility.toObject(errorProperty);

	     int statusCode = error.get("httpCode").asInt();
	     String message = error.get("errorDescription").asText();

	     ErrorResponseDto errorResponseDto = new ErrorResponseDto(errorCode, message);

	     response.setStatus(statusCode);
	     response.setContentType("application/json");
	     response.setCharacterEncoding("UTF-8");

	     response.getWriter().write(JsonUtility.toJson(errorResponseDto));
	 }
}
