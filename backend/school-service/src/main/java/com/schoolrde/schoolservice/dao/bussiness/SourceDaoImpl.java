package com.schoolrde.schoolservice.dao.bussiness;

import java.util.List;
import java.util.Optional;
import org.springframework.stereotype.Repository;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.schoolrde.schoolservice.dao.repository.SourceRepository;
import com.schoolrde.schoolservice.entity.SourceEntity;
import com.schoolrde.schoolservice.util.JsonUtility;

@Repository
public class SourceDaoImpl implements SourceDao{

    private static final Logger LOGGER = LoggerFactory.getLogger(SourceDaoImpl.class);

    private final SourceRepository sourceRepository;

    public SourceDaoImpl(SourceRepository sourceRepository){
        this.sourceRepository=sourceRepository;
    }

    @Override
    public List<SourceEntity> findSourceBySchoolId(Integer schoolId){
        LOGGER.info("Quering source from database with schoolId : {}", schoolId);
        return sourceRepository.findBySchoolId(schoolId);
    }

    @Override
    public Optional<SourceEntity> findSourceById(Integer id){
        LOGGER.info("Quering source from database with id : {}", id);
        return sourceRepository.findById(id);
    }

    @Override
    public SourceEntity saveSource(SourceEntity sourceEntity){
        LOGGER.info("source to be saved into DB : {}", JsonUtility.toJson(sourceEntity));
        SourceEntity savedSourceEntity=sourceRepository.save(sourceEntity);
        LOGGER.info("source saved successfully : {}", JsonUtility.toJson(savedSourceEntity));
        return savedSourceEntity;
    }

}
