package com.schoolrde.schoolservice.service;

import java.util.List;
import java.util.stream.Collectors;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import com.schoolrde.schoolservice.dao.bussiness.SchoolDao;
import com.schoolrde.schoolservice.dto.SchoolRequestDto;
import com.schoolrde.schoolservice.dto.SchoolResponseDto;
import com.schoolrde.schoolservice.entity.SchoolEntity;
import com.schoolrde.schoolservice.exception.CustomException;

@Service
public class SchoolService{
	
    private static final Logger LOGGER=LoggerFactory.getLogger(SchoolService.class);
    
    @Autowired
    SchoolDao schoolDao;

    public SchoolResponseDto getSchoolById(String schoolId){
    	LOGGER.debug("Fetching school with schoolId : {}", schoolId);

        SchoolEntity schoolEntity=schoolDao.findBySchoolId(schoolId)
                .orElseThrow(()->{
                	LOGGER.warn("School not found with schoolId : {}", schoolId);
                    return new CustomException("E9001");
                });

        LOGGER.info("School retrieved successfully with schoolId : {}",schoolId);
        return convertToResponseDto(schoolEntity);
    }
    
    
    public Long createSchool(SchoolRequestDto schoolRequestDto){
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
        LOGGER.info("Creating SchoolResponseDto");
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
}