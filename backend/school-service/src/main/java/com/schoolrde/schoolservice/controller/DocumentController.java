package com.schoolrde.schoolservice.controller;


import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import com.schoolrde.schoolservice.dto.DocumentRequestDto;
import com.schoolrde.schoolservice.dto.DocumentResponseDto;
import com.schoolrde.schoolservice.dto.RequestLoggerDto;
import com.schoolrde.schoolservice.dto.ResponseLoggerDto;
import com.schoolrde.schoolservice.service.DocumentService;
import com.schoolrde.schoolservice.util.JsonUtility;

import jakarta.servlet.http.HttpServletRequest;


@RestController
@RequestMapping("${spring.application.name}/document")
public class DocumentController{

	private static final Logger LOGGER = LoggerFactory.getLogger(DocumentController.class);

	private final DocumentService documentService;

	public DocumentController(DocumentService documentService){
	    this.documentService = documentService;
	}

	@GetMapping("/getDocument/objectId")
	public ResponseEntity<List<DocumentResponseDto>> getDocumentByObjectIdAndCategoryId(@RequestParam Integer objectId, @RequestParam Integer objectCategoryId, HttpServletRequest request) throws Exception{

	    String uri = request.getRequestURI();
	    String method = request.getMethod();

	    RequestLoggerDto requestLoggerDto = new RequestLoggerDto();
	    requestLoggerDto.setApi(uri);
	    requestLoggerDto.setMethod(method);
	    requestLoggerDto.setRequestBody("{\"objectId\":\"" + objectId + "\",\"objectCategoryId\":\"" + objectCategoryId + "\"}");

	    LOGGER.info("Request: {}", JsonUtility.toJson(requestLoggerDto));

	    List<DocumentResponseDto> responseDto = documentService.getDocumentByObjectIdAndObjectCategoryId(objectId, objectCategoryId);

	    ResponseLoggerDto responseLoggerDto = new ResponseLoggerDto();
	    responseLoggerDto.setApi(uri);
	    responseLoggerDto.setMethod(method);
	    responseLoggerDto.setStatusCode(HttpStatus.OK.value());
	    responseLoggerDto.setResponseBody(JsonUtility.toJson(responseDto));

	    LOGGER.info("Response: {}", JsonUtility.toJson(responseLoggerDto));

	    return ResponseEntity.ok(responseDto);
	}

	@GetMapping("/getDocument/id")
	public ResponseEntity<DocumentResponseDto> getDocumentById(@RequestParam Integer id, HttpServletRequest request) throws Exception{

	    String uri = request.getRequestURI();
	    String method = request.getMethod();

	    RequestLoggerDto requestLoggerDto = new RequestLoggerDto();
	    requestLoggerDto.setApi(uri);
	    requestLoggerDto.setMethod(method);
	    requestLoggerDto.setRequestBody("{\"id\":\"" + id + "\"}");

	    LOGGER.info("Request: {}", JsonUtility.toJson(requestLoggerDto));

	    DocumentResponseDto responseDto = documentService.getDocumentById(id);

	    ResponseLoggerDto responseLoggerDto = new ResponseLoggerDto();
	    responseLoggerDto.setApi(uri);
	    responseLoggerDto.setMethod(method);
	    responseLoggerDto.setStatusCode(HttpStatus.OK.value());
	    responseLoggerDto.setResponseBody(JsonUtility.toJson(responseDto));

	    LOGGER.info("Response: {}", JsonUtility.toJson(responseLoggerDto));

	    return ResponseEntity.ok(responseDto);
	}

	@PostMapping("/createDocument")
	public ResponseEntity<Integer> createDocument(@RequestBody DocumentRequestDto documentRequestDto, HttpServletRequest request) throws Exception{

	    String uri = request.getRequestURI();
	    String method = request.getMethod();

	    RequestLoggerDto requestLoggerDto = new RequestLoggerDto();
	    requestLoggerDto.setApi(uri);
	    requestLoggerDto.setMethod(method);
	    requestLoggerDto.setRequestBody(JsonUtility.toJson(documentRequestDto));

	    LOGGER.info("Request: {}", JsonUtility.toJson(requestLoggerDto));

	    Integer id = documentService.createDocument(documentRequestDto);

	    ResponseLoggerDto responseLoggerDto = new ResponseLoggerDto();
	    responseLoggerDto.setApi(uri);
	    responseLoggerDto.setMethod(method);
	    responseLoggerDto.setStatusCode(HttpStatus.CREATED.value());
	    responseLoggerDto.setResponseBody("{\"id\":\"" + id + "\"}");

	    LOGGER.info("Response: {}", JsonUtility.toJson(responseLoggerDto));

	    return ResponseEntity.status(HttpStatus.CREATED).body(id);
	}
}