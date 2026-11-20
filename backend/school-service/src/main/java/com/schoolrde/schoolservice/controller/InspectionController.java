package com.schoolrde.schoolservice.controller;

import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import com.schoolrde.schoolservice.dto.InspectionRequestDto;
import com.schoolrde.schoolservice.dto.InspectionResponseDto;
import com.schoolrde.schoolservice.dto.RequestLoggerDto;
import com.schoolrde.schoolservice.dto.ResponseLoggerDto;
import com.schoolrde.schoolservice.service.InspectionService;
import com.schoolrde.schoolservice.util.JsonUtility;

import jakarta.servlet.http.HttpServletRequest;


@RestController
@RequestMapping("${spring.application.name}/inspection")
public class InspectionController{

	private static final Logger LOGGER = LoggerFactory.getLogger(InspectionController.class);

	private final InspectionService inspectionService;

	public InspectionController(InspectionService inspectionService){
	    this.inspectionService = inspectionService;
	}

	@GetMapping("/getInspection/schoolId")
	public ResponseEntity<List<InspectionResponseDto>> getInspectionBySchoolId(@RequestParam Integer schoolId, HttpServletRequest request) throws Exception{

	    String uri = request.getRequestURI();
	    String method = request.getMethod();

	    RequestLoggerDto requestLoggerDto = new RequestLoggerDto();
	    requestLoggerDto.setApi(uri);
	    requestLoggerDto.setMethod(method);
	    requestLoggerDto.setRequestBody(JsonUtility.toJson(schoolId));

	    LOGGER.info("Request: {}", JsonUtility.toJson(requestLoggerDto));

	    List<InspectionResponseDto> responseDto = inspectionService.getInspectionBySchoolId(schoolId);

	    ResponseLoggerDto responseLoggerDto = new ResponseLoggerDto();
	    responseLoggerDto.setApi(uri);
	    responseLoggerDto.setMethod(method);
	    responseLoggerDto.setStatusCode(HttpStatus.OK.value());
	    responseLoggerDto.setResponseBody(JsonUtility.toJson(responseDto));

	    LOGGER.info("Response: {}", JsonUtility.toJson(responseLoggerDto));

	    return ResponseEntity.ok(responseDto);
	}

	@GetMapping("/getInspection/id")
	public ResponseEntity<InspectionResponseDto> getInspectionById(@RequestParam Integer id, HttpServletRequest request) throws Exception{

	    String uri = request.getRequestURI();
	    String method = request.getMethod();

	    RequestLoggerDto requestLoggerDto = new RequestLoggerDto();
	    requestLoggerDto.setApi(uri);
	    requestLoggerDto.setMethod(method);
	    requestLoggerDto.setRequestBody("{\"id\":\"" + id + "\"}");

	    LOGGER.info("Request: {}", JsonUtility.toJson(requestLoggerDto));

	    InspectionResponseDto responseDto = inspectionService.getInspectionById(id);

	    ResponseLoggerDto responseLoggerDto = new ResponseLoggerDto();
	    responseLoggerDto.setApi(uri);
	    responseLoggerDto.setMethod(method);
	    responseLoggerDto.setStatusCode(HttpStatus.OK.value());
	    responseLoggerDto.setResponseBody(JsonUtility.toJson(responseDto));

	    LOGGER.info("Response: {}", JsonUtility.toJson(responseLoggerDto));

	    return ResponseEntity.ok(responseDto);
	}

	@PostMapping("/createInspection")
	public ResponseEntity<Integer> createInspection(@RequestBody InspectionRequestDto inspectionRequestDto, HttpServletRequest request) throws Exception{

	    String uri = request.getRequestURI();
	    String method = request.getMethod();

	    RequestLoggerDto requestLoggerDto = new RequestLoggerDto();
	    requestLoggerDto.setApi(uri);
	    requestLoggerDto.setMethod(method);
	    requestLoggerDto.setRequestBody(JsonUtility.toJson(inspectionRequestDto));

	    LOGGER.info("Request: {}", JsonUtility.toJson(requestLoggerDto));

	    Integer id = inspectionService.createInspection(inspectionRequestDto);

	    ResponseLoggerDto responseLoggerDto = new ResponseLoggerDto();
	    responseLoggerDto.setApi(uri);
	    responseLoggerDto.setMethod(method);
	    responseLoggerDto.setStatusCode(HttpStatus.CREATED.value());
	    responseLoggerDto.setResponseBody("{\"id\":\"" + id + "\"}");

	    LOGGER.info("Response: {}", JsonUtility.toJson(responseLoggerDto));

	    return ResponseEntity.status(HttpStatus.CREATED).body(id);
	}
}