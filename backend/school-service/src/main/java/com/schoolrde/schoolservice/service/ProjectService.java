package com.schoolrde.schoolservice.service;
//DTO-to-Entity and Entity-to-DTO mapping is implemented with AI assistance

import java.util.ArrayList;
import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import com.schoolrde.schoolservice.dao.bussiness.ProjectDao;
import com.schoolrde.schoolservice.dto.DocumentResponseDto;
import com.schoolrde.schoolservice.dto.ProjectRequestDto;
import com.schoolrde.schoolservice.dto.ProjectResponseDto;
import com.schoolrde.schoolservice.dto.TenderResponseDto;
import com.schoolrde.schoolservice.entity.ProjectEntity;
import com.schoolrde.schoolservice.entity.TenderEntity;
import com.schoolrde.schoolservice.exception.CustomException;


@Service
public class ProjectService{
	
	private static final Logger LOGGER = LoggerFactory.getLogger(ProjectService.class);
	
	public static final Integer CATEGORY_PROJECT = 4;
	public static final Integer CATEGORY_TENDER = 5;

	private final ProjectDao projectDao;
    private final DocumentService documentService;


	public ProjectService(ProjectDao projectDao, DocumentService documentService){
	    this.projectDao = projectDao;
	    this.documentService = documentService;
	}

	
	public List<ProjectResponseDto> getProjectByIssueId(Integer issueId){

	    LOGGER.info("Fetching projects for issueId: {}", issueId);

	    List<ProjectEntity> projectEntities = projectDao.findProjectByIssueId(issueId);

	    if(projectEntities.isEmpty()){
	        LOGGER.warn("Projects not found for issueId: {}", issueId);
	        throw new CustomException("E9007");
	    }

	    List<ProjectResponseDto> projectResponseDtos = new ArrayList<>();

	    for(ProjectEntity projectEntity : projectEntities){
	        projectResponseDtos.add(convertToProjectResponseDto(projectEntity));
	    }

	    return projectResponseDtos;
	}

	public ProjectResponseDto getProjectById(Integer id){

	    LOGGER.info("Fetching project with id: {}", id);

	    ProjectEntity projectEntity = projectDao.findProjectById(id)
	                    .orElseThrow(()->{
	                        LOGGER.warn("Project not found with id: {}", id);
	                        return new CustomException("E9007");
	                    });

	    return convertToProjectResponseDto(projectEntity);
	}

	public Integer createProject(ProjectRequestDto projectRequestDto){

	    LOGGER.info("Creating project");

	    ProjectEntity projectEntity = new ProjectEntity();
	    projectEntity.setIssueId(projectRequestDto.getIssueId());
	    projectEntity.setProjectType(projectRequestDto.getProjectType());
	    projectEntity.setProjectDescription(projectRequestDto.getProjectDescription());
	    projectEntity.setProjectStatus(projectRequestDto.getProjectStatus());
	    projectEntity.setEstimatedCost(projectRequestDto.getEstimatedCost());
	    projectEntity.setActualCost(projectRequestDto.getActualCost());
	    projectEntity.setStartDate(projectRequestDto.getStartDate());
	    projectEntity.setExpectedCompletionDate(projectRequestDto.getExpectedCompletionDate());
	    projectEntity.setActualCompletionDate(projectRequestDto.getActualCompletionDate());
	    projectEntity.setRemarks(projectRequestDto.getRemarks());

	    ProjectEntity savedEntity = projectDao.saveProject(projectEntity);

	    LOGGER.info("Project created successfully with id: {}", savedEntity.getId());

	    return savedEntity.getId();
	}

	private ProjectResponseDto convertToProjectResponseDto(ProjectEntity projectEntity){

	    LOGGER.info("Converting ProjectEntity to ProjectResponseDto");

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
	    List<DocumentResponseDto> projectDocuments = documentService
	    		.getDocumentByObjectIdAndObjectCategoryId(projectEntity.getId(), CATEGORY_PROJECT);
	    projectResponseDto.setProjectDocuments(projectDocuments);

	    List<TenderEntity> tenderEntities = projectEntity.getTenders();
	    
	    List<TenderResponseDto> tenderResponseDtos = new ArrayList<>();

	    for(TenderEntity tenderEntity : tenderEntities){
	        TenderResponseDto tenderResponseDto = new TenderResponseDto();

	        tenderResponseDto.setId(tenderEntity.getId());
	        tenderResponseDto.setProjectId(tenderEntity.getProjectId());
	        tenderResponseDto.setTenderNumber(tenderEntity.getTenderNumber());
	        tenderResponseDto.setTenderTitle(tenderEntity.getTenderTitle());
	        tenderResponseDto.setTenderDescription(tenderEntity.getTenderDescription());
	        tenderResponseDto.setTenderStatus(tenderEntity.getTenderStatus().getStatus());
	        tenderResponseDto.setEstimatedAmount(tenderEntity.getEstimatedAmount());
	        tenderResponseDto.setAwardedAmount(tenderEntity.getAwardedAmount());
	        tenderResponseDto.setPublicationDate(tenderEntity.getPublicationDate());
	        tenderResponseDto.setSubmissionDeadline(tenderEntity.getSubmissionDeadline());
	        tenderResponseDto.setAwardDate(tenderEntity.getAwardDate());
	        tenderResponseDto.setContractorName(tenderEntity.getContractorName());
	        tenderResponseDto.setContractStartDate(tenderEntity.getContractStartDate());
	        tenderResponseDto.setContractEndDate(tenderEntity.getContractEndDate());
		    List<DocumentResponseDto> tenderDocuments = documentService
		    		.getDocumentByObjectIdAndObjectCategoryId(tenderEntity.getId(), CATEGORY_TENDER);
		    tenderResponseDto.setTenderDocuments(tenderDocuments);

	        tenderResponseDtos.add(tenderResponseDto);
	    }
	    projectResponseDto.setTenders(tenderResponseDtos);

	    return projectResponseDto;
	}
}
