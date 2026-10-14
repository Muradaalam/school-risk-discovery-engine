package com.schoolrde.schoolservice.controller;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.web.csrf.CsrfToken;
import org.springframework.web.bind.annotation.*;

import com.schoolrde.schoolservice.dto.RequestLoggerDto;
import com.schoolrde.schoolservice.dto.ResponseLoggerDto;
import com.schoolrde.schoolservice.dto.SchoolRequestDto;
import com.schoolrde.schoolservice.dto.SchoolResponseDto;
import com.schoolrde.schoolservice.service.SchoolService;
import com.schoolrde.schoolservice.util.JsonUtility;

import jakarta.servlet.http.HttpServletRequest; 

@RestController
@RequestMapping("${spring.application.name}")
public class SchoolController{
    
	private static final Logger LOGGER = LoggerFactory.getLogger(SchoolController.class);
    
	@Autowired
	SchoolService schoolService;

	@GetMapping("/csrf-token")
	public CsrfToken getCsrfToken(CsrfToken csrfToken) {
	    return csrfToken;
	}
	
    @GetMapping("/getSchool/{schoolId}")
    public ResponseEntity<SchoolResponseDto> getSchoolById(@PathVariable String schoolId, HttpServletRequest request) throws Exception{
    	String uri = request.getRequestURI();
    	String method = request.getMethod();
    	
    	RequestLoggerDto requestLoggerDto = new RequestLoggerDto();
    	requestLoggerDto.setApi(uri);
    	requestLoggerDto.setMethod(method);
    	requestLoggerDto.setRequestBody("{\"schoolId\":\"" + schoolId + "\"}");
    	LOGGER.info("Request : {}", JsonUtility.toJson(requestLoggerDto));

    	SchoolResponseDto schoolResponseDto = schoolService.getSchoolById(schoolId);

        ResponseLoggerDto responseLoggerDto = new ResponseLoggerDto();
    	responseLoggerDto.setApi(uri);
    	responseLoggerDto.setMethod(method);
    	responseLoggerDto.setStatusCode(HttpStatus.OK.value());
    	responseLoggerDto.setResponseBody(JsonUtility.toJson(schoolResponseDto));
    	LOGGER.info("Response: {}", JsonUtility.toJson(responseLoggerDto));
    	
    	return ResponseEntity.ok(schoolResponseDto);
}
    @PostMapping("/createSchool")
    public ResponseEntity<Long> createSchool(@RequestBody SchoolRequestDto schoolRequestDto, HttpServletRequest request) throws Exception{
    	String uri = request.getRequestURI();
    	String method = request.getMethod();
    	
    	RequestLoggerDto requestLoggerDto = new RequestLoggerDto();
    	requestLoggerDto.setApi(uri);
    	requestLoggerDto.setMethod(method);
    	requestLoggerDto.setRequestBody(JsonUtility.toJson(schoolRequestDto));
    	LOGGER.info("Request : {}", JsonUtility.toJson(requestLoggerDto));

    	Long id = schoolService.createSchool(schoolRequestDto);
    	
        ResponseLoggerDto responseLoggerDto = new ResponseLoggerDto();
    	responseLoggerDto.setApi(uri);
    	responseLoggerDto.setMethod(method);
    	responseLoggerDto.setStatusCode(HttpStatus.OK.value());
    	responseLoggerDto.setResponseBody("{\"id\":\"" + id + "\"}");
    	LOGGER.info("Response: {}", JsonUtility.toJson(responseLoggerDto));

        return ResponseEntity.status(HttpStatus.CREATED).body(id);
    }


    @DeleteMapping("/deleteSchool/{schoolId}")
    public ResponseEntity<String> deleteSchool(@PathVariable String schoolId, HttpServletRequest request) throws Exception{
    	LOGGER.info("Request to delete school with schoolId : {}",schoolId);
    	String uri = request.getRequestURI();
    	String method = request.getMethod();
    	
    	RequestLoggerDto requestLoggerDto = new RequestLoggerDto();
    	requestLoggerDto.setApi(uri);
    	requestLoggerDto.setMethod(method);
    	requestLoggerDto.setRequestBody("{\"schoolId\":\"" + schoolId + "\"}");

    	schoolService.deleteSchool(schoolId);

        ResponseLoggerDto responseLoggerDto = new ResponseLoggerDto();
    	responseLoggerDto.setApi(uri);
    	responseLoggerDto.setMethod(method);
    	responseLoggerDto.setStatusCode(HttpStatus.OK.value());
    	responseLoggerDto.setResponseBody("{\"schoolId\":\"" + schoolId + "\"}");
    	LOGGER.info("Response: {}", JsonUtility.toJson(responseLoggerDto));
    	return ResponseEntity.ok("School with schoolId " + schoolId + " deleted successfully");
    }
}