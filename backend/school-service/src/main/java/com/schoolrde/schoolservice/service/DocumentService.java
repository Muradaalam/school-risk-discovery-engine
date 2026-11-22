package com.schoolrde.schoolservice.service;

import java.util.ArrayList;
import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import com.schoolrde.schoolservice.dao.bussiness.DocumentDao;
import com.schoolrde.schoolservice.dao.bussiness.SourceDao;
import com.schoolrde.schoolservice.dao.repository.ObjectCategoryRepository;
import com.schoolrde.schoolservice.dto.DocumentRequestDto;
import com.schoolrde.schoolservice.dto.DocumentResponseDto;
import com.schoolrde.schoolservice.dto.SourceResponseDto;
import com.schoolrde.schoolservice.entity.DocumentEntity;
import com.schoolrde.schoolservice.entity.ObjectCategory;
import com.schoolrde.schoolservice.entity.SourceEntity;
import com.schoolrde.schoolservice.exception.CustomException;


@Service
public class DocumentService{
	
	private static final Logger LOGGER = LoggerFactory.getLogger(DocumentService.class);

	private final DocumentDao documentDao;
	private final ObjectCategoryRepository objectCategoryRepository;
	private final SourceDao sourceDao;

	public DocumentService(DocumentDao documentDao, ObjectCategoryRepository objectCategoryRepository, SourceDao sourceDao){
	    this.documentDao = documentDao;
	    this.objectCategoryRepository = objectCategoryRepository;
	    this.sourceDao = sourceDao;
	}

	public List<DocumentResponseDto> getDocumentByObjectIdAndObjectCategoryId(Integer objectId, Integer objectCategoryId){

	    LOGGER.info("Fetching documents for objectId: {} and objectCategoryId: {}", objectId, objectCategoryId);

	    List<DocumentEntity> documentEntities = documentDao.findDocumentByObjectIdAndObjectCategoryId(objectId, objectCategoryId);

	    List<DocumentResponseDto> documentResponseDtos = new ArrayList<>();

	    if(documentEntities.isEmpty()){
	        LOGGER.warn("Documents not found for objectId: {} and objectCategoryId: {}", objectId, objectCategoryId);
	        return documentResponseDtos;
	    }

	    for(DocumentEntity documentEntity : documentEntities){
	        documentResponseDtos.add(convertToDocumentResponseDto(documentEntity));
	    }
	    return documentResponseDtos;
	}

	public List<DocumentResponseDto> getDocumentBySourceId(Integer sourceId){

	    LOGGER.info("Fetching documents for sourceId: {}", sourceId);

	    List<DocumentEntity> documentEntities = documentDao.findDocumentBySourceId(sourceId);

	    if(documentEntities.isEmpty()){
	        LOGGER.warn("Documents not found for sourceId: {}", sourceId);
	        return new ArrayList<>();
	    }

	    List<DocumentResponseDto> documentResponseDtos = new ArrayList<>();

	    for(DocumentEntity documentEntity : documentEntities){
	        documentResponseDtos.add(convertToDocumentResponseDto(documentEntity));
	    }

	    return documentResponseDtos;
	}

	public DocumentResponseDto getDocumentById(Integer id){

	    LOGGER.info("Fetching document with id: {}", id);

	    DocumentEntity documentEntity = documentDao.findDocumentById(id)
	                    .orElseThrow(()->{
	                        LOGGER.warn("Document not found with id: {}", id);
	                        return new CustomException("E9007");
	                    });

	    return convertToDocumentResponseDto(documentEntity);
	}

	public Integer createDocument(DocumentRequestDto documentRequestDto){

	    LOGGER.info("Creating document");

	    DocumentEntity documentEntity = new DocumentEntity();
	    documentEntity.setObjectId(documentRequestDto.getObjectId());
	    ObjectCategory objectCategory = objectCategoryRepository.findByObjectName(documentRequestDto.getObjectCategory())
	    		.orElseGet(()->{
	                LOGGER.warn("Object category not found: {}, setting category to OTHER", documentRequestDto.getObjectCategory());

	                return objectCategoryRepository.findByObjectName("OTHER")
	                        .orElseThrow(()-> new CustomException("E9007"));
	            });
	    documentEntity.setObjectCategoryId(objectCategory.getId());
	    documentEntity.setSourceId(documentRequestDto.getSourceId());
	    documentEntity.setDocumentName(documentRequestDto.getDocumentName());
	    documentEntity.setDocPath(documentRequestDto.getDocPath());
	    documentEntity.setDescription(documentRequestDto.getDescription());

	    DocumentEntity savedEntity = documentDao.saveDocument(documentEntity);

	    LOGGER.info("Document created successfully with id: {}", savedEntity.getId());

	    return savedEntity.getId();
	}

	private DocumentResponseDto convertToDocumentResponseDto(DocumentEntity documentEntity){

	    LOGGER.info("Converting DocumentEntity to DocumentResponseDto");

	    DocumentResponseDto documentResponseDto = new DocumentResponseDto();

	    documentResponseDto.setId(documentEntity.getId());
	    documentResponseDto.setObjectId(documentEntity.getObjectId());
	    ObjectCategory objectCategory = objectCategoryRepository.findById(documentEntity.getObjectCategoryId())
	            .orElseGet(()->{
	                LOGGER.warn("Object category not found: {}, setting category to OTHER", documentEntity.getObjectCategoryId());

	                return objectCategoryRepository.findByObjectName("OTHER")
	                        .orElseThrow(()-> new CustomException("E9007"));
	            });
	    documentResponseDto.setObjectCategory(objectCategory.getObjectName());
	    if(documentEntity.getSourceId() != null){
	        SourceEntity sourceEntity = sourceDao.findSourceById(documentEntity.getSourceId())
	        		.orElseGet(()->{
	                    LOGGER.warn("Source not found: {}", documentEntity.getSourceId());
	                    return null;
	                });

	        if (sourceEntity != null){
	        SourceResponseDto sourceResponseDto = new SourceResponseDto();

	        sourceResponseDto.setId(sourceEntity.getId());
	        sourceResponseDto.setSourceName(sourceEntity.getSourceName().getSourceName());
	        sourceResponseDto.setSourceUrl(sourceEntity.getSourceUrl());
	        sourceResponseDto.setPublicationDate(sourceEntity.getPublicationDate());

	        documentResponseDto.setSource(sourceResponseDto);
	        }
	    }

	    documentResponseDto.setDocumentName(documentEntity.getDocumentName());
	    documentResponseDto.setDocPath(documentEntity.getDocPath());
	    documentResponseDto.setDescription(documentEntity.getDescription());

	    return documentResponseDto;
	}
}
