package com.schoolrde.schoolservice.controller;

import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import com.schoolrde.schoolservice.dto.ProjectRequestDto;
import com.schoolrde.schoolservice.dto.ProjectResponseDto;
import com.schoolrde.schoolservice.dto.RequestLoggerDto;
import com.schoolrde.schoolservice.dto.ResponseLoggerDto;
import com.schoolrde.schoolservice.service.ProjectService;
import com.schoolrde.schoolservice.util.JsonUtility;

import jakarta.servlet.http.HttpServletRequest;

@RestController
@RequestMapping("${spring.application.name}/project")
public class ProjectController{

	private static final Logger LOGGER = LoggerFactory.getLogger(ProjectController.class);

	private final ProjectService projectService;

	public ProjectController(ProjectService projectService){
	    this.projectService = projectService;
	}

	@GetMapping("/getProject/issueId")
	public ResponseEntity<List<ProjectResponseDto>> getProjectByIssueId(@RequestParam Integer issueId, HttpServletRequest request) throws Exception{

	    String uri = request.getRequestURI();
	    String method = request.getMethod();

	    RequestLoggerDto requestLoggerDto = new RequestLoggerDto();
	    requestLoggerDto.setApi(uri);
	    requestLoggerDto.setMethod(method);
	    requestLoggerDto.setRequestBody(JsonUtility.toJson(issueId));

	    LOGGER.info("Request: {}", JsonUtility.toJson(requestLoggerDto));

	    List<ProjectResponseDto> responseDto = projectService.getProjectByIssueId(issueId);

	    ResponseLoggerDto responseLoggerDto = new ResponseLoggerDto();
	    responseLoggerDto.setApi(uri);
	    responseLoggerDto.setMethod(method);
	    responseLoggerDto.setStatusCode(HttpStatus.OK.value());
	    responseLoggerDto.setResponseBody(JsonUtility.toJson(responseDto));

	    LOGGER.info("Response: {}", JsonUtility.toJson(responseLoggerDto));

	    return ResponseEntity.ok(responseDto);
	}

	@GetMapping("/getProject/id")
	public ResponseEntity<ProjectResponseDto> getProjectById(@RequestParam Integer id, HttpServletRequest request) throws Exception{

	    String uri = request.getRequestURI();
	    String method = request.getMethod();

	    RequestLoggerDto requestLoggerDto = new RequestLoggerDto();
	    requestLoggerDto.setApi(uri);
	    requestLoggerDto.setMethod(method);
	    requestLoggerDto.setRequestBody("{\"id\":\"" + id + "\"}");

	    LOGGER.info("Request: {}", JsonUtility.toJson(requestLoggerDto));

	    ProjectResponseDto responseDto = projectService.getProjectById(id);

	    ResponseLoggerDto responseLoggerDto = new ResponseLoggerDto();
	    responseLoggerDto.setApi(uri);
	    responseLoggerDto.setMethod(method);
	    responseLoggerDto.setStatusCode(HttpStatus.OK.value());
	    responseLoggerDto.setResponseBody(JsonUtility.toJson(responseDto));

	    LOGGER.info("Response: {}", JsonUtility.toJson(responseLoggerDto));

	    return ResponseEntity.ok(responseDto);
	}

	@PostMapping("/createProject")
	public ResponseEntity<Integer> createProject(@RequestBody ProjectRequestDto projectRequestDto, HttpServletRequest request) throws Exception{

	    String uri = request.getRequestURI();
	    String method = request.getMethod();

	    RequestLoggerDto requestLoggerDto = new RequestLoggerDto();
	    requestLoggerDto.setApi(uri);
	    requestLoggerDto.setMethod(method);
	    requestLoggerDto.setRequestBody(JsonUtility.toJson(projectRequestDto));

	    LOGGER.info("Request: {}", JsonUtility.toJson(requestLoggerDto));

	    Integer id = projectService.createProject(projectRequestDto);

	    ResponseLoggerDto responseLoggerDto = new ResponseLoggerDto();
	    responseLoggerDto.setApi(uri);
	    responseLoggerDto.setMethod(method);
	    responseLoggerDto.setStatusCode(HttpStatus.CREATED.value());
	    responseLoggerDto.setResponseBody("{\"id\":\"" + id + "\"}");

	    LOGGER.info("Response: {}", JsonUtility.toJson(responseLoggerDto));

	    return ResponseEntity.status(HttpStatus.CREATED).body(id);
	}
}