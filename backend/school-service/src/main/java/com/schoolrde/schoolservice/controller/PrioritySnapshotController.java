package com.schoolrde.schoolservice.controller;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import com.schoolrde.schoolservice.dto.PrioritySnapshotRequestDto;
import com.schoolrde.schoolservice.dto.PrioritySnapshotResponseDto;
import com.schoolrde.schoolservice.dto.RequestLoggerDto;
import com.schoolrde.schoolservice.dto.ResponseLoggerDto;
import com.schoolrde.schoolservice.service.PrioritySnapshotService;
import com.schoolrde.schoolservice.util.JsonUtility;

import jakarta.servlet.http.HttpServletRequest;

@RestController
@RequestMapping("${spring.application.name}/prioritySnapshot")
public class PrioritySnapshotController{

	private static final Logger LOGGER = LoggerFactory.getLogger(PrioritySnapshotController.class);

	private final PrioritySnapshotService prioritySnapshotService;

	public PrioritySnapshotController(PrioritySnapshotService prioritySnapshotService){
	    this.prioritySnapshotService = prioritySnapshotService;
	}

	@GetMapping("/getPrioritySnapshot/schoolId")
	public ResponseEntity<PrioritySnapshotResponseDto> getPrioritySnapshotBySchoolId(@RequestParam Integer schoolId, HttpServletRequest request) throws Exception{

	    String uri = request.getRequestURI();
	    String method = request.getMethod();

	    RequestLoggerDto requestLoggerDto = new RequestLoggerDto();
	    requestLoggerDto.setApi(uri);
	    requestLoggerDto.setMethod(method);
	    requestLoggerDto.setRequestBody(JsonUtility.toJson(schoolId));

	    LOGGER.info("Request: {}", JsonUtility.toJson(requestLoggerDto));

	    PrioritySnapshotResponseDto responseDto = prioritySnapshotService.getPrioritySnapshotBySchoolId(schoolId);

	    ResponseLoggerDto responseLoggerDto = new ResponseLoggerDto();
	    responseLoggerDto.setApi(uri);
	    responseLoggerDto.setMethod(method);
	    responseLoggerDto.setStatusCode(HttpStatus.OK.value());
	    responseLoggerDto.setResponseBody(JsonUtility.toJson(responseDto));

	    LOGGER.info("Response: {}", JsonUtility.toJson(responseLoggerDto));

	    return ResponseEntity.ok(responseDto);
	}

	@GetMapping("/getPrioritySnapshot/id")
	public ResponseEntity<PrioritySnapshotResponseDto> getPrioritySnapshotById(@RequestParam Integer id, HttpServletRequest request) throws Exception{

	    String uri = request.getRequestURI();
	    String method = request.getMethod();

	    RequestLoggerDto requestLoggerDto = new RequestLoggerDto();
	    requestLoggerDto.setApi(uri);
	    requestLoggerDto.setMethod(method);
	    requestLoggerDto.setRequestBody("{\"id\":\"" + id + "\"}");

	    LOGGER.info("Request: {}", JsonUtility.toJson(requestLoggerDto));

	    PrioritySnapshotResponseDto responseDto = prioritySnapshotService.getPrioritySnapshotById(id);

	    ResponseLoggerDto responseLoggerDto = new ResponseLoggerDto();
	    responseLoggerDto.setApi(uri);
	    responseLoggerDto.setMethod(method);
	    responseLoggerDto.setStatusCode(HttpStatus.OK.value());
	    responseLoggerDto.setResponseBody(JsonUtility.toJson(responseDto));

	    LOGGER.info("Response: {}", JsonUtility.toJson(responseLoggerDto));

	    return ResponseEntity.ok(responseDto);
	}

	@PostMapping("/createPrioritySnapshot")
	public ResponseEntity<Integer> createPrioritySnapshot(@RequestBody PrioritySnapshotRequestDto prioritySnapshotRequestDto, HttpServletRequest request) throws Exception{

	    String uri = request.getRequestURI();
	    String method = request.getMethod();

	    RequestLoggerDto requestLoggerDto = new RequestLoggerDto();
	    requestLoggerDto.setApi(uri);
	    requestLoggerDto.setMethod(method);
	    requestLoggerDto.setRequestBody(JsonUtility.toJson(prioritySnapshotRequestDto));

	    LOGGER.info("Request: {}", JsonUtility.toJson(requestLoggerDto));

	    Integer id = prioritySnapshotService.createPrioritySnapshot(prioritySnapshotRequestDto);

	    ResponseLoggerDto responseLoggerDto = new ResponseLoggerDto();
	    responseLoggerDto.setApi(uri);
	    responseLoggerDto.setMethod(method);
	    responseLoggerDto.setStatusCode(HttpStatus.CREATED.value());
	    responseLoggerDto.setResponseBody("{\"id\":\"" + id + "\"}");

	    LOGGER.info("Response: {}", JsonUtility.toJson(responseLoggerDto));

	    return ResponseEntity.status(HttpStatus.CREATED).body(id);
	}
}