package com.schoolrde.schoolservice.controller;

import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import com.schoolrde.schoolservice.dto.RequestLoggerDto;
import com.schoolrde.schoolservice.dto.ResponseLoggerDto;
import com.schoolrde.schoolservice.dto.SourceRequestDto;
import com.schoolrde.schoolservice.dto.SourceResponseDto;
import com.schoolrde.schoolservice.service.SourceService;
import com.schoolrde.schoolservice.util.JsonUtility;

import jakarta.servlet.http.HttpServletRequest;


@RestController
@RequestMapping("${spring.application.name}/source")
public class SourceController{

	private static final Logger LOGGER = LoggerFactory.getLogger(SourceController.class);

	private final SourceService sourceService;

	public SourceController(SourceService sourceService){
	    this.sourceService = sourceService;
	}

	@GetMapping("/getSource/schoolId")
	public ResponseEntity<List<SourceResponseDto>> getSourceBySchoolId(@RequestParam Integer schoolId, HttpServletRequest request) throws Exception{

	    String uri = request.getRequestURI();
	    String method = request.getMethod();

	    RequestLoggerDto requestLoggerDto = new RequestLoggerDto();
	    requestLoggerDto.setApi(uri);
	    requestLoggerDto.setMethod(method);
	    requestLoggerDto.setRequestBody(JsonUtility.toJson(schoolId));

	    LOGGER.info("Request: {}", JsonUtility.toJson(requestLoggerDto));

	    List<SourceResponseDto> responseDto = sourceService.getSourceBySchoolId(schoolId);

	    ResponseLoggerDto responseLoggerDto = new ResponseLoggerDto();
	    responseLoggerDto.setApi(uri);
	    responseLoggerDto.setMethod(method);
	    responseLoggerDto.setStatusCode(HttpStatus.OK.value());
	    responseLoggerDto.setResponseBody(JsonUtility.toJson(responseDto));

	    LOGGER.info("Response: {}", JsonUtility.toJson(responseLoggerDto));

	    return ResponseEntity.ok(responseDto);
	}

	@GetMapping("/getSource/id")
	public ResponseEntity<SourceResponseDto> getSourceById(@RequestParam Integer id, HttpServletRequest request) throws Exception{

	    String uri = request.getRequestURI();
	    String method = request.getMethod();

	    RequestLoggerDto requestLoggerDto = new RequestLoggerDto();
	    requestLoggerDto.setApi(uri);
	    requestLoggerDto.setMethod(method);
	    requestLoggerDto.setRequestBody("{\"id\":\"" + id + "\"}");

	    LOGGER.info("Request: {}", JsonUtility.toJson(requestLoggerDto));

	    SourceResponseDto responseDto = sourceService.getSourceById(id);

	    ResponseLoggerDto responseLoggerDto = new ResponseLoggerDto();
	    responseLoggerDto.setApi(uri);
	    responseLoggerDto.setMethod(method);
	    responseLoggerDto.setStatusCode(HttpStatus.OK.value());
	    responseLoggerDto.setResponseBody(JsonUtility.toJson(responseDto));

	    LOGGER.info("Response: {}", JsonUtility.toJson(responseLoggerDto));

	    return ResponseEntity.ok(responseDto);
	}

	@PostMapping("/createSource")
	public ResponseEntity<Integer> createSource(@RequestBody SourceRequestDto sourceRequestDto, HttpServletRequest request) throws Exception{

	    String uri = request.getRequestURI();
	    String method = request.getMethod();

	    RequestLoggerDto requestLoggerDto = new RequestLoggerDto();
	    requestLoggerDto.setApi(uri);
	    requestLoggerDto.setMethod(method);
	    requestLoggerDto.setRequestBody(JsonUtility.toJson(sourceRequestDto));

	    LOGGER.info("Request: {}", JsonUtility.toJson(requestLoggerDto));

	    Integer id = sourceService.createSource(sourceRequestDto);

	    ResponseLoggerDto responseLoggerDto = new ResponseLoggerDto();
	    responseLoggerDto.setApi(uri);
	    responseLoggerDto.setMethod(method);
	    responseLoggerDto.setStatusCode(HttpStatus.CREATED.value());
	    responseLoggerDto.setResponseBody("{\"id\":\"" + id + "\"}");

	    LOGGER.info("Response: {}", JsonUtility.toJson(responseLoggerDto));

	    return ResponseEntity.status(HttpStatus.CREATED).body(id);
	}
}