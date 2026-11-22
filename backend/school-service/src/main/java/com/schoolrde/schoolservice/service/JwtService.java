package com.schoolrde.schoolservice.service;
//JwtService file is implemented with AI assistance 

import java.util.Date;

import javax.crypto.SecretKey;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.io.Decoders;
import io.jsonwebtoken.security.Keys;

@Service
public class JwtService{

	private static final Logger LOGGER = LoggerFactory.getLogger(JwtService.class);

	@Value("${jwt.secret}")
	private String secretKey;

	@Value("${jwt.expiration}")
	private long jwtExpiration;


	private SecretKey getSigningKey(){
		byte[] keyBytes = Decoders.BASE64.decode(secretKey);
	    return Keys.hmacShaKeyFor(keyBytes);
	}


	public String generateToken(String username){

	    LOGGER.info("Generating JWT token for username : {}", username);

	    Date currentDate = new Date();
	    Date expiryDate = new Date(currentDate.getTime() + jwtExpiration);
	    String token = Jwts.builder().subject(username).issuedAt(currentDate).expiration(expiryDate)
	    		.signWith(getSigningKey()).compact();

	    LOGGER.info("JWT token generated successfully for username : {}", username);

	    return token;
	}


	public String extractUsername(String token){

	    LOGGER.info("Extracting username from JWT token");

	    return extractClaims(token).getSubject();
	}


	public boolean validateToken(String token){

	    LOGGER.info("Validating JWT token");

	    try{
	        Claims claims = extractClaims(token);
	        return claims.getExpiration().after(new Date());
	    }catch(io.jsonwebtoken.JwtException | IllegalArgumentException ex){

	        LOGGER.warn("Invalid JWT token : {}", ex.getMessage());
	        return false;
	    }
	}


	private Claims extractClaims(String token){
	    return Jwts.parser().verifyWith(getSigningKey()).build().parseSignedClaims(token)
	    		.getPayload();
	}
}