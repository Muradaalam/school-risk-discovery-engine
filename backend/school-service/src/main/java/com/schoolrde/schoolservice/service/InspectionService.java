package com.schoolrde.schoolservice.service;

import java.util.ArrayList;
import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import com.schoolrde.schoolservice.dao.bussiness.InspectionDao;
import com.schoolrde.schoolservice.dto.DocumentResponseDto;
import com.schoolrde.schoolservice.dto.InspectionRequestDto;
import com.schoolrde.schoolservice.dto.InspectionResponseDto;
import com.schoolrde.schoolservice.entity.InspectionEntity;
import com.schoolrde.schoolservice.exception.CustomException;


@Service
public class InspectionService{
	
	private static final Logger LOGGER = LoggerFactory.getLogger(InspectionService.class);
	
	public static final Integer CATEGORY_INSPECTION = 6;

	private final InspectionDao inspectionDao;
    private final DocumentService documentService;

	public InspectionService(InspectionDao inspectionDao, DocumentService documentService){
	    this.inspectionDao = inspectionDao;
	    this.documentService = documentService;
	}

	
	public List<InspectionResponseDto> getInspectionBySchoolId(Integer schoolId){

	    LOGGER.info("Fetching inspections for schoolId: {}", schoolId);

	    List<InspectionEntity> inspectionEntities = inspectionDao.findInspectionBySchoolId(schoolId);

	    if(inspectionEntities.isEmpty()){
	        LOGGER.warn("Inspections not found for schoolId: {}", schoolId);
	        throw new CustomException("E9007");
	    }

	    List<InspectionResponseDto> inspectionResponseDtos = new ArrayList<>();

	    for(InspectionEntity inspectionEntity : inspectionEntities){
	        inspectionResponseDtos.add(convertToInspectionResponseDto(inspectionEntity));
	    }

	    return inspectionResponseDtos;
	}

	public InspectionResponseDto getInspectionById(Integer id){

	    LOGGER.info("Fetching inspection with id: {}", id);

	    InspectionEntity inspectionEntity = inspectionDao.findInspectionById(id)
	                    .orElseThrow(()->{
	                        LOGGER.warn("Inspection not found with id: {}", id);
	                        return new CustomException("E9007");
	                    });

	    return convertToInspectionResponseDto(inspectionEntity);
	}

	public Integer createInspection(InspectionRequestDto inspectionRequestDto){

	    LOGGER.info("Creating inspection");

	    InspectionEntity inspectionEntity = new InspectionEntity();
	    inspectionEntity.setSchoolId(inspectionRequestDto.getSchoolId());
	    inspectionEntity.setInspectionDate(inspectionRequestDto.getInspectionDate());
	    inspectionEntity.setInspectionType(inspectionRequestDto.getInspectionType());
	    inspectionEntity.setRemarks(inspectionRequestDto.getRemarks());
	    inspectionEntity.setInspectorName(inspectionRequestDto.getInspectorName());

	    InspectionEntity savedEntity = inspectionDao.saveInspection(inspectionEntity);

	    LOGGER.info("Inspection created successfully with id: {}", savedEntity.getId());

	    return savedEntity.getId();
	}

	private InspectionResponseDto convertToInspectionResponseDto(InspectionEntity inspectionEntity){

	    LOGGER.info("Converting InspectionEntity to InspectionResponseDto");

	    InspectionResponseDto inspectionResponseDto = new InspectionResponseDto();

	    inspectionResponseDto.setId(inspectionEntity.getId());
	    inspectionResponseDto.setInspectionDate(inspectionEntity.getInspectionDate());
	    inspectionResponseDto.setInspectionType(inspectionEntity.getInspectionType());
	    inspectionResponseDto.setRemarks(inspectionEntity.getRemarks());
	    inspectionResponseDto.setInspectorName(inspectionEntity.getInspectorName());
	    List<DocumentResponseDto> inspectionDocuments = documentService
	    		.getDocumentByObjectIdAndObjectCategoryId(inspectionEntity.getId(), CATEGORY_INSPECTION);
	    inspectionResponseDto.setInspectionDocuments(inspectionDocuments);

	    return inspectionResponseDto;
	}
}
