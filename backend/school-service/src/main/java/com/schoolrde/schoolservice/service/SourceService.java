package com.schoolrde.schoolservice.service;

import java.util.ArrayList;
import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import com.schoolrde.schoolservice.dao.bussiness.SourceDao;
import com.schoolrde.schoolservice.dto.SourceRequestDto;
import com.schoolrde.schoolservice.dto.SourceResponseDto;
import com.schoolrde.schoolservice.entity.SourceEntity;
import com.schoolrde.schoolservice.entity.SourceName;
import com.schoolrde.schoolservice.exception.CustomException;

import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;


@Service
public class SourceService{
	
	private static final Logger LOGGER = LoggerFactory.getLogger(SourceService.class);

	private final SourceDao sourceDao;

	public SourceService(SourceDao sourceDao){
	    this.sourceDao = sourceDao;
	}

	@PersistenceContext
	private EntityManager entityManager;

	
	public List<SourceResponseDto> getSourceBySchoolId(Integer schoolId){

	    LOGGER.info("Fetching sources for schoolId: {}", schoolId);

	    List<SourceEntity> sourceEntities = sourceDao.findSourceBySchoolId(schoolId);

	    if(sourceEntities.isEmpty()){
	        LOGGER.warn("Sources not found for schoolId: {}", schoolId);
	        throw new CustomException("E9007");
	    }

	    List<SourceResponseDto> sourceResponseDtos = new ArrayList<>();

	    for(SourceEntity sourceEntity : sourceEntities){
	        sourceResponseDtos.add(convertToSourceResponseDto(sourceEntity));
	    }

	    return sourceResponseDtos;
	}

	public SourceResponseDto getSourceById(Integer id){

	    LOGGER.info("Fetching source with id: {}", id);

	    SourceEntity sourceEntity = sourceDao.findSourceById(id)
	                    .orElseThrow(()->{
	                        LOGGER.warn("Source not found with id: {}", id);
	                        return new CustomException("E9007");
	                    });

	    return convertToSourceResponseDto(sourceEntity);
	}

	public Integer createSource(SourceRequestDto sourceRequestDto){

	    LOGGER.info("Creating source");

	    SourceEntity sourceEntity = new SourceEntity();
	    sourceEntity.setSchoolId(sourceRequestDto.getSchoolId());

	    SourceName sourceName = entityManager.getReference(SourceName.class, sourceRequestDto.getSourceNameId());
	    sourceEntity.setSourceName(sourceName);
	    sourceEntity.setSourceUrl(sourceRequestDto.getSourceUrl());
	    sourceEntity.setPublicationDate(sourceRequestDto.getPublicationDate());

	    SourceEntity savedEntity = sourceDao.saveSource(sourceEntity);

	    LOGGER.info("Source created successfully with id: {}", savedEntity.getId());

	    return savedEntity.getId();
	}

	private SourceResponseDto convertToSourceResponseDto(SourceEntity sourceEntity){

	    LOGGER.info("Converting SourceEntity to SourceResponseDto");

	    SourceResponseDto sourceResponseDto = new SourceResponseDto();

	    sourceResponseDto.setId(sourceEntity.getId());
	    sourceResponseDto.setSourceUrl(sourceEntity.getSourceUrl());
	    sourceResponseDto.setPublicationDate(sourceEntity.getPublicationDate());

	    return sourceResponseDto;
	}
}
