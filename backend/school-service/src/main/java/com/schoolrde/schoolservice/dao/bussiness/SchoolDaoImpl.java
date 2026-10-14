package com.schoolrde.schoolservice.dao.bussiness;


import java.util.Optional;
import org.springframework.stereotype.Repository;
import com.schoolrde.schoolservice.dao.repository.SchoolRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;


import com.schoolrde.schoolservice.entity.SchoolEntity;
import com.schoolrde.schoolservice.util.JsonUtility;

@Repository
public class SchoolDaoImpl implements SchoolDao{

	private static final Logger LOGGER = LoggerFactory.getLogger(SchoolDaoImpl.class);

	private final SchoolRepository schoolRepository;

    public SchoolDaoImpl(SchoolRepository schoolRepository){
        this.schoolRepository=schoolRepository;
    }

    @Override
    public Optional<SchoolEntity> findBySchoolId(String schoolId){
    	LOGGER.info("Quering school from database with schoolId : {}", schoolId);
        return schoolRepository.findBySchoolId(schoolId);
    }
    
    @Override
    public SchoolEntity save(SchoolEntity schoolEntity){
    	LOGGER.info("School to be saved into DB : {}", JsonUtility.toJson(schoolEntity));
        SchoolEntity savedSchool=schoolRepository.save(schoolEntity);
        LOGGER.info("School saved successfully : {}", JsonUtility.toJson(savedSchool));
        return savedSchool;
    }

    @Override
    public boolean existsBySchoolId(String schoolId){
    	LOGGER.info("Checking school in DB with schoolId : {}", schoolId);
        return schoolRepository.existsBySchoolId(schoolId);
    }

    @Override
    public void deleteBySchoolId(String schoolId){
    	LOGGER.info("Deleting school from DB with schoolId : {}", schoolId);
        schoolRepository.deleteBySchoolId(schoolId);
        LOGGER.info("Delete operation is completed for schoolId : {}", schoolId);
    }
}