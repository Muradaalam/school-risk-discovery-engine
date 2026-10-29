package com.schoolrde.schoolservice.service;

import java.util.List;
import java.util.stream.Collectors;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import com.schoolrde.schoolservice.dao.bussiness.SchoolDao;
import com.schoolrde.schoolservice.dto.IssueResponseDto;
import com.schoolrde.schoolservice.dto.ProjectResponseDto;
import com.schoolrde.schoolservice.dto.SchoolRequestDto;
import com.schoolrde.schoolservice.dto.SchoolResponseDto;
import com.schoolrde.schoolservice.dto.SchoolWithIssueResponseDto;
import com.schoolrde.schoolservice.dto.TenderResponseDto;
import com.schoolrde.schoolservice.entity.IssueEntity;
import com.schoolrde.schoolservice.entity.ProjectEntity;
import com.schoolrde.schoolservice.entity.SchoolEntity;
import com.schoolrde.schoolservice.entity.SchoolWithIssueEntity;
import com.schoolrde.schoolservice.entity.TenderEntity;
import com.schoolrde.schoolservice.exception.CustomException;

@Service
public class SchoolService{
	
    private static final Logger LOGGER=LoggerFactory.getLogger(SchoolService.class);
    
    @Autowired
    SchoolDao schoolDao;
    
    public SchoolResponseDto getSchoolBySchoolId(String schoolId){
    	LOGGER.debug("Fetching school with schoolId : {}", schoolId);

        SchoolEntity schoolEntity=schoolDao.findBySchoolId(schoolId)
                .orElseThrow(()->{
                	LOGGER.warn("School not found with schoolId : {}", schoolId);
                    return new CustomException("E9001");
                });

        LOGGER.info("School retrieved successfully with schoolId : {}",schoolId);
        return convertToResponseDto(schoolEntity);
    }
    

    public SchoolWithIssueResponseDto getSchoolById(int id){
    	LOGGER.debug("Fetching school with Id : {}", id);

    	SchoolWithIssueEntity schoolWithIssueEntity=schoolDao.findById(id)
                .orElseThrow(()->{
                	LOGGER.warn("School not found with Id : {}", id);
                    return new CustomException("E9001");
                });

        LOGGER.info("School retrieved successfully with Id : {}",id);
        return convertToSchoolWithIssueResponseDto(schoolWithIssueEntity);
    }
    
    public Integer createSchool(SchoolRequestDto schoolRequestDto){
        if(schoolRequestDto.getSchoolId() == null || schoolRequestDto.getSchoolId().isBlank()){
        	LOGGER.warn("School creation failed: schoolId is missing");
            throw new CustomException("E9003");
        }

        if(schoolRequestDto.getSchoolName() == null || schoolRequestDto.getSchoolName().isBlank()){
        	LOGGER.warn("School creation failed: schoolName is missing for schoolId : {}",schoolRequestDto.getSchoolId());
            throw new CustomException("E9004");
        }

        if(schoolDao.existsBySchoolId(schoolRequestDto.getSchoolId())){
        	LOGGER.warn("School creation failed: duplicate schoolId : {}", schoolRequestDto.getSchoolId());
            throw new CustomException("E9002");
        }

        try{
            SchoolEntity schoolEntity=new SchoolEntity();
            schoolEntity.setSchoolId(schoolRequestDto.getSchoolId());
            schoolEntity.setUdiseCode(schoolRequestDto.getUdiseCode());
            schoolEntity.setSchoolName(schoolRequestDto.getSchoolName());
            schoolEntity.setState(schoolRequestDto.getState());
            schoolEntity.setDistrict(schoolRequestDto.getDistrict());
            schoolEntity.setBlock(schoolRequestDto.getBlock());
            schoolEntity.setLatitude(schoolRequestDto.getLatitude());
            schoolEntity.setLongitude(schoolRequestDto.getLongitude());
            schoolEntity.setSchoolType(schoolRequestDto.getSchoolType());
            schoolEntity.setManagementType(schoolRequestDto.getManagementType());

            
            SchoolEntity savedSchool=schoolDao.save(schoolEntity);
                        
           
            LOGGER.info("School created successfully with schoolId : {}", schoolRequestDto.getSchoolId());
            return savedSchool.getId();
            
        }catch(CustomException ex){
        	LOGGER.error("Error : Failed to create school with schoolId : {}", schoolRequestDto.getSchoolId(),ex);
            throw ex;
        }catch(Exception ex){
        	LOGGER.error("Error : Failed to create school with schoolId : {}", schoolRequestDto.getSchoolId(),ex);
            throw ex;
        }
    }
    
    @Transactional
    public void deleteSchool(String schoolId){
    	LOGGER.debug("Deleting school with schoolId : {}",schoolId);

        SchoolEntity schoolEntity=schoolDao.findBySchoolId(schoolId)
                .orElseThrow(()->{
                	LOGGER.warn("School deletion failed: school not found with schoolId : {}", schoolId);
                    return new CustomException("E9005");
                });

        schoolDao.deleteBySchoolId(schoolEntity.getSchoolId());
        LOGGER.info("School deleted successfully with schoolId : {}", schoolId);
    }

    private SchoolResponseDto convertToResponseDto(SchoolEntity schoolEntity){
        LOGGER.info("Creating SchoolResponseDto...");
        SchoolResponseDto schoolResponseDto=new SchoolResponseDto();
        schoolResponseDto.setId(schoolEntity.getId());
        schoolResponseDto.setSchoolId(schoolEntity.getSchoolId());
        schoolResponseDto.setUdiseCode(schoolEntity.getUdiseCode());
        schoolResponseDto.setSchoolName(schoolEntity.getSchoolName());
        schoolResponseDto.setState(schoolEntity.getState());
        schoolResponseDto.setDistrict(schoolEntity.getDistrict());
        schoolResponseDto.setBlock(schoolEntity.getBlock());
        schoolResponseDto.setLatitude(schoolEntity.getLatitude());
        schoolResponseDto.setLongitude(schoolEntity.getLongitude());
        schoolResponseDto.setSchoolType(schoolEntity.getSchoolType());
        schoolResponseDto.setManagementType(schoolEntity.getManagementType());
        schoolResponseDto.setCreatedOn(schoolEntity.getCreatedOn());
        schoolResponseDto.setCreatedBy(schoolEntity.getCreatedBy());
        schoolResponseDto.setUpdatedOn(schoolEntity.getUpdatedOn());
        schoolResponseDto.setUpdatedBy(schoolEntity.getUpdatedBy());
        return schoolResponseDto;
    }
    
    private SchoolWithIssueResponseDto convertToSchoolWithIssueResponseDto(SchoolWithIssueEntity schoolWithIssueEntity){
    	
    	LOGGER.info("Creating SchoolWithIssueResponseDto...");
        SchoolWithIssueResponseDto schoolWithIssueResponseDto = new SchoolWithIssueResponseDto();

        schoolWithIssueResponseDto.setId(schoolWithIssueEntity.getId());
        schoolWithIssueResponseDto.setSchoolId(schoolWithIssueEntity.getSchoolId());
        schoolWithIssueResponseDto.setUdiseCode(schoolWithIssueEntity.getUdiseCode());
        schoolWithIssueResponseDto.setSchoolName(schoolWithIssueEntity.getSchoolName());
        schoolWithIssueResponseDto.setState(schoolWithIssueEntity.getState());
        schoolWithIssueResponseDto.setDistrict(schoolWithIssueEntity.getDistrict());
        schoolWithIssueResponseDto.setBlock(schoolWithIssueEntity.getBlock());
        schoolWithIssueResponseDto.setLatitude(schoolWithIssueEntity.getLatitude());
        schoolWithIssueResponseDto.setLongitude(schoolWithIssueEntity.getLongitude());
        schoolWithIssueResponseDto.setSchoolType(schoolWithIssueEntity.getSchoolType());
        schoolWithIssueResponseDto.setManagementType(schoolWithIssueEntity.getManagementType());

        List<IssueResponseDto> issues = schoolWithIssueEntity.getIssues()
                .stream().map(this::convertToIssueResponseDto)
                .collect(Collectors.toList());

        schoolWithIssueResponseDto.setIssues(issues);

        return schoolWithIssueResponseDto;
    }

    private IssueResponseDto convertToIssueResponseDto(IssueEntity issueEntity) {

    	LOGGER.info("Creating IssueResponseDto...");
        IssueResponseDto issueResponseDto = new IssueResponseDto();

        issueResponseDto.setId(issueEntity.getId());
        issueResponseDto.setFirstDetected(issueEntity.getFirstDetected());
        issueResponseDto.setLastUpdated(issueEntity.getLastUpdated());
        issueResponseDto.setResolvedAt(issueEntity.getResolvedAt());
        issueResponseDto.setIssueType(issueEntity.getIssueType().getIssue_type());
        issueResponseDto.setIssueTypeDescription(issueEntity.getIssueType().getDescription());
        issueResponseDto.setStatus(issueEntity.getIssueStatus().getStatus());
        issueResponseDto.setStatusDescription(issueEntity.getIssueStatus().getDescription());

        List<ProjectResponseDto> projects = issueEntity.getProjects()
                .stream().map(this::convertToProjectResponseDto)
                .collect(Collectors.toList());

        issueResponseDto.setProjects(projects);
        return issueResponseDto;
    }
    
    private ProjectResponseDto convertToProjectResponseDto(ProjectEntity projectEntity){

    	LOGGER.info("Creating ProjectResponseDto...");
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
        List<TenderResponseDto> tenders = projectEntity.getTenders()
                .stream().map(this::convertToTenderResponseDto)
                .collect(Collectors.toList());

        projectResponseDto.setTenders(tenders);        

        return projectResponseDto;
    }
    
    private TenderResponseDto convertToTenderResponseDto(TenderEntity tenderEntity){

        
    	LOGGER.info("Creating TenderResponseDto...");
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

        return tenderResponseDto;
    }
    
}