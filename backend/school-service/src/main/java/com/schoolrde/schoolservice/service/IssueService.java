package com.schoolrde.schoolservice.service;

import java.util.ArrayList;
import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import com.schoolrde.schoolservice.dao.bussiness.IssueDao;
import com.schoolrde.schoolservice.dao.bussiness.ProjectDao;
import com.schoolrde.schoolservice.dto.IssueRequestDto;
import com.schoolrde.schoolservice.dto.IssueResponseDto;
import com.schoolrde.schoolservice.dto.ProjectResponseDto;
import com.schoolrde.schoolservice.entity.IssueEntity;
import com.schoolrde.schoolservice.entity.IssueType;
import com.schoolrde.schoolservice.entity.ProjectEntity;
import com.schoolrde.schoolservice.exception.CustomException;

import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;


@Service
public class IssueService{
	
	private static final Logger LOGGER = LoggerFactory.getLogger(IssueService.class);

	private final IssueDao issueDao;
	private final ProjectDao projectDao;

	public IssueService(IssueDao issueDao, ProjectDao projectDao){
	    this.issueDao = issueDao;
	    this.projectDao = projectDao;
	}

	@PersistenceContext
	private EntityManager entityManager;

	
	public List<IssueResponseDto> getIssueBySchoolId(Integer schoolId){

	    LOGGER.info("Fetching issues for schoolId: {}", schoolId);

	    List<IssueEntity> issueEntities = issueDao.findIssueBySchoolId(schoolId);

	    if(issueEntities.isEmpty()){
	        LOGGER.warn("Issues not found for schoolId: {}", schoolId);
	        throw new CustomException("E9007");
	    }

	    List<IssueResponseDto> issueResponseDtos = new ArrayList<>();

	    for(IssueEntity issueEntity : issueEntities){
	        issueResponseDtos.add(convertToIssueResponseDto(issueEntity));
	    }

	    return issueResponseDtos;
	}

	public IssueResponseDto getIssueById(Integer id){

	    LOGGER.info("Fetching issue with id: {}", id);

	    IssueEntity issueEntity = issueDao.findIssueById(id)
	                    .orElseThrow(()->{
	                        LOGGER.warn("Issue not found with id: {}", id);
	                        return new CustomException("E9007");
	                    });

	    return convertToIssueResponseDto(issueEntity);
	}

	public Integer createIssue(IssueRequestDto issueRequestDto){

	    LOGGER.info("Creating issue");

	    IssueEntity issueEntity = new IssueEntity();
	    issueEntity.setSchoolId(issueRequestDto.getSchoolId());

	    IssueType issueType = entityManager.getReference(IssueType.class, issueRequestDto.getIssueTypeId());
	    issueEntity.setIssueType(issueType);
	    issueEntity.setStatusId(issueRequestDto.getStatusId());
	    issueEntity.setFirstDetected(issueRequestDto.getFirstDetected());
	    issueEntity.setLastUpdated(issueRequestDto.getLastUpdated());
	    issueEntity.setResolvedAt(issueRequestDto.getResolvedAt());

	    IssueEntity savedEntity = issueDao.saveIssue(issueEntity);

	    LOGGER.info("Issue created successfully with id: {}", savedEntity.getId());

	    return savedEntity.getId();
	}

	private IssueResponseDto convertToIssueResponseDto(IssueEntity issueEntity){

	    LOGGER.info("Converting IssueEntity to IssueResponseDto");

	    IssueResponseDto issueResponseDto = new IssueResponseDto();

	    issueResponseDto.setId(issueEntity.getId());
	    issueResponseDto.setFirstDetected(issueEntity.getFirstDetected());
	    issueResponseDto.setLastUpdated(issueEntity.getLastUpdated());
	    issueResponseDto.setResolvedAt(issueEntity.getResolvedAt());

	    List<ProjectEntity> projectEntities = projectDao.findProjectByIssueId(issueEntity.getId());

	    List<ProjectResponseDto> projectResponseDtos = new ArrayList<>();

	    for(ProjectEntity projectEntity : projectEntities){
	        ProjectResponseDto projectResponseDto = new ProjectResponseDto();

	        projectResponseDto.setId(projectEntity.getId());
	        projectResponseDto.setIssueId(projectEntity.getIssueId());
	        projectResponseDto.setProjectType(projectEntity.getProjectType());
	        projectResponseDto.setProjectDescription(projectEntity.getProjectDescription());
	        projectResponseDto.setProjectStatus(projectEntity.getProjectStatus());
	        projectResponseDto.setEstimatedCost(projectEntity.getEstimatedCost());
	        projectResponseDto.setActualCost(projectEntity.getActualCost());
	        projectResponseDto.setStartDate(projectEntity.getStartDate());
	        projectResponseDto.setExpectedCompletionDate(projectEntity.getExpectedCompletionDate());
	        projectResponseDto.setActualCompletionDate(projectEntity.getActualCompletionDate());
	        projectResponseDto.setRemarks(projectEntity.getRemarks());

	        projectResponseDtos.add(projectResponseDto);
	    }

	    issueResponseDto.setProjects(projectResponseDtos);

	    return issueResponseDto;
	}
}
