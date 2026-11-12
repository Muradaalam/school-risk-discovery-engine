package com.schoolrde.schoolservice.service;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import com.schoolrde.schoolservice.dao.bussiness.PrioritySnapshotDao;
import com.schoolrde.schoolservice.dto.PrioritySnapshotRequestDto;
import com.schoolrde.schoolservice.dto.PrioritySnapshotResponseDto;
import com.schoolrde.schoolservice.entity.PrioritySnapshotEntity;
import com.schoolrde.schoolservice.exception.CustomException;


@Service
public class PrioritySnapshotService{
	
	private static final Logger LOGGER = LoggerFactory.getLogger(PrioritySnapshotService.class);

	private final PrioritySnapshotDao prioritySnapshotDao;

	public PrioritySnapshotService(PrioritySnapshotDao prioritySnapshotDao){
	    this.prioritySnapshotDao = prioritySnapshotDao;
	}

	
	public PrioritySnapshotResponseDto getPrioritySnapshotBySchoolId(Integer schoolId){

	    LOGGER.info("Fetching priority snapshot for schoolId: {}", schoolId);

	    PrioritySnapshotEntity prioritySnapshotEntity = prioritySnapshotDao.findPrioritySnapshotBySchoolId(schoolId)
	                    .orElseThrow(()->{
	                        LOGGER.warn("Priority snapshot not found for schoolId: {}", schoolId);
	                        return new CustomException("E9007");
	                    });
	    
	    return convertToPrioritySnapshotResponseDto(prioritySnapshotEntity);
	}

	public PrioritySnapshotResponseDto getPrioritySnapshotById(Integer id){

	    LOGGER.info("Fetching priority snapshot with id: {}", id);

	    PrioritySnapshotEntity prioritySnapshotEntity =
	            prioritySnapshotDao.findPrioritySnapshotById(id)
	                    .orElseThrow(()->{
	                        LOGGER.warn("Priority snapshot not found with id: {}", id);
	                        return new CustomException("E9007");
	                    });

	    return convertToPrioritySnapshotResponseDto(prioritySnapshotEntity);
	}

	public Integer createPrioritySnapshot(PrioritySnapshotRequestDto prioritySnapshotRequestDto){

	    LOGGER.info("Creating priority snapshot");

	    PrioritySnapshotEntity prioritySnapshotEntity = new PrioritySnapshotEntity();
	    prioritySnapshotEntity.setSchoolId(prioritySnapshotRequestDto.getSchoolId());
	    prioritySnapshotEntity.setSnapshotDate(prioritySnapshotRequestDto.getSnapshotDate());
	    prioritySnapshotEntity.setPriorityScore(prioritySnapshotRequestDto.getPriorityScore());
	    prioritySnapshotEntity.setActiveIssues(prioritySnapshotRequestDto.getActiveIssues());
	    prioritySnapshotEntity.setUnderResolutionIssues(prioritySnapshotRequestDto.getUnderResolutionIssues());
	    prioritySnapshotEntity.setResolvedIssues(prioritySnapshotRequestDto.getResolvedIssues());

	    PrioritySnapshotEntity savedEntity = prioritySnapshotDao.savePrioritySnapshot(prioritySnapshotEntity);

	    LOGGER.info("Priority snapshot created successfully with id: {}", savedEntity.getId());

	    return savedEntity.getId();
	}

	private PrioritySnapshotResponseDto convertToPrioritySnapshotResponseDto(PrioritySnapshotEntity prioritySnapshotEntity){

	    LOGGER.info("Converting PrioritySnapshotEntity to PrioritySnapshotResponseDto");

	    PrioritySnapshotResponseDto responseDto = new PrioritySnapshotResponseDto();

	    responseDto.setId(prioritySnapshotEntity.getId());
	    responseDto.setSnapshotDate(prioritySnapshotEntity.getSnapshotDate());
	    responseDto.setPriorityScore(prioritySnapshotEntity.getPriorityScore());
	    responseDto.setActiveIssues(prioritySnapshotEntity.getActiveIssues());
	    responseDto.setUnderResolutionIssues(prioritySnapshotEntity.getUnderResolutionIssues());
	    responseDto.setResolvedIssues(prioritySnapshotEntity.getResolvedIssues());

	    return responseDto;
	}
}