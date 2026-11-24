package com.schoolrde.schoolservice.dao.bussiness;

import java.util.List;
import java.util.Optional;
import org.springframework.stereotype.Repository;

import com.schoolrde.schoolservice.dao.repository.InspectionRepository;
import com.schoolrde.schoolservice.entity.InspectionEntity;
import com.schoolrde.schoolservice.util.JsonUtility;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;


@Repository
public class InspectionDaoImpl implements InspectionDao{

    private static final Logger LOGGER = LoggerFactory.getLogger(InspectionDaoImpl.class);

    private final InspectionRepository inspectionRepository;

    public InspectionDaoImpl(InspectionRepository inspectionRepository){
        this.inspectionRepository=inspectionRepository;
    }

    @Override
    public List<InspectionEntity> findInspectionBySchoolId(Integer schoolId){
        LOGGER.info("Quering inspection from database with schoolId : {}", schoolId);
        return inspectionRepository.findBySchoolId(schoolId);
    }

    @Override
    public Optional<InspectionEntity> findInspectionById(Integer id){
        LOGGER.info("Quering inspection from database with id : {}", id);
        return inspectionRepository.findById(id);
    }

    @Override
    public InspectionEntity saveInspection(InspectionEntity inspectionEntity){
        LOGGER.info("inspection to be saved into DB : {}", JsonUtility.toJson(inspectionEntity));
        InspectionEntity savedInspectionEntity=inspectionRepository.save(inspectionEntity);
        LOGGER.info("inspection saved successfully : {}", JsonUtility.toJson(savedInspectionEntity));
        return savedInspectionEntity;
    }

}
