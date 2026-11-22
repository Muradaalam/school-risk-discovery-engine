package com.schoolrde.schoolservice.service;

import java.util.ArrayList;
import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import com.schoolrde.schoolservice.dao.bussiness.IssueDao;
import com.schoolrde.schoolservice.dao.repository.IssueStatusRepository;
import com.schoolrde.schoolservice.dao.repository.IssueTypeRepository;
import com.schoolrde.schoolservice.dto.DocumentResponseDto;
import com.schoolrde.schoolservice.dto.IssueRequestDto;
import com.schoolrde.schoolservice.dto.IssueResponseDto;
import com.schoolrde.schoolservice.dto.ProjectResponseDto;
import com.schoolrde.schoolservice.entity.IssueEntity;
import com.schoolrde.schoolservice.entity.IssueStatus;
import com.schoolrde.schoolservice.entity.IssueType;
import com.schoolrde.schoolservice.entity.ProjectEntity;
import com.schoolrde.schoolservice.exception.CustomException;


@Service
public class IssueService{
	
	private static final Logger LOGGER = LoggerFactory.getLogger(IssueService.class);
	
	public static final Integer CATEGORY_ISSUE = 2;

	private final IssueDao issueDao;
	private final DocumentService documentService;
	private final IssueTypeRepository issueTypeRepository;
	private final IssueStatusRepository issueStatusRepository;

	public IssueService(IssueDao issueDao, DocumentService documentService, IssueTypeRepository issueTypeRepository, IssueStatusRepository issueStatusRepository){
	    this.issueDao = issueDao;
	    this.documentService = documentService;
	    this.issueTypeRepository = issueTypeRepository;
	    this.issueStatusRepository = issueStatusRepository;
	}
	
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

	    IssueType issueType = issueTypeRepository.findByIssueType(issueRequestDto.getIssueType())
	            .orElseGet(()->{
	                LOGGER.warn("Issue type is not found with id: {}, setting issue type to OTHER", issueRequestDto.getIssueType());
	                return issueTypeRepository.findByIssueType("OTHER")
	                        .orElseThrow(()-> new CustomException("E9007"));
	            });
	    issueEntity.setIssueType(issueType);
	    IssueStatus issueStatus = issueStatusRepository.findByStatus(issueRequestDto.getIssueStatus())
	            .orElseGet(()->{
	                LOGGER.warn("Issue status is not found with id: {}, setting issue status to UNKNOWN", issueRequestDto.getIssueStatus());
	                return issueStatusRepository.findByStatus("UNKNOWN")
	                        .orElseThrow(()-> new CustomException("E9007"));
	            });
	    issueEntity.setIssueStatus(issueStatus);
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
        issueResponseDto.setIssueType(issueEntity.getIssueType().getIssueType());
        issueResponseDto.setIssueTypeDescription(issueEntity.getIssueType().getDescription());
        issueResponseDto.setStatus(issueEntity.getIssueStatus().getStatus());
        issueResponseDto.setStatusDescription(issueEntity.getIssueStatus().getDescription());
	    issueResponseDto.setFirstDetected(issueEntity.getFirstDetected());
	    issueResponseDto.setLastUpdated(issueEntity.getLastUpdated());
	    issueResponseDto.setResolvedAt(issueEntity.getResolvedAt());

	    List<ProjectEntity> projectEntities = issueEntity.getProjects();
	    
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
	    List<DocumentResponseDto> issueDocuments = documentService
	    		.getDocumentByObjectIdAndObjectCategoryId(issueEntity.getId(), CATEGORY_ISSUE);
	    issueResponseDto.setIssueDocuments(issueDocuments);

	    return issueResponseDto;
	}
}
