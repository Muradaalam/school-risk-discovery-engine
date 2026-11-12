package com.schoolrde.schoolservice.dao.bussiness;


import java.util.Optional;
import org.springframework.stereotype.Repository;

import com.schoolrde.schoolservice.dao.repository.PrioritySnapshotRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;


import com.schoolrde.schoolservice.entity.PrioritySnapshotEntity;
import com.schoolrde.schoolservice.util.JsonUtility;

@Repository
public class PrioritySnapshotDaoImpl implements PrioritySnapshotDao{

	private static final Logger LOGGER = LoggerFactory.getLogger(PrioritySnapshotDaoImpl.class);

	private final PrioritySnapshotRepository prioritySnapshotRepository;

    public PrioritySnapshotDaoImpl(PrioritySnapshotRepository prioritySnapshotRepository){
        this.prioritySnapshotRepository=prioritySnapshotRepository;
    }

    @Override
    public Optional<PrioritySnapshotEntity> findPrioritySnapshotBySchoolId(Integer schoolId){
    	LOGGER.info("Quering prioritySnapshot from database with schoolId : {}", schoolId);
        return prioritySnapshotRepository.findBySchoolId(schoolId);
    }
    
    @Override
    public Optional<PrioritySnapshotEntity> findPrioritySnapshotById(Integer id){
    	LOGGER.info("Quering prioritySnapshot from database with id : {}", id);
        return prioritySnapshotRepository.findById(id);
    }
    
    @Override
    public PrioritySnapshotEntity savePrioritySnapshot(PrioritySnapshotEntity prioritySnapshotEntity){
    	LOGGER.info("prioritySnapshot to be saved into DB : {}", JsonUtility.toJson(prioritySnapshotEntity));
    	PrioritySnapshotEntity savedPrioritySnapshotEntity=prioritySnapshotRepository.save(prioritySnapshotEntity);
        LOGGER.info("prioritySnapshot saved successfully : {}", JsonUtility.toJson(savedPrioritySnapshotEntity));
        return savedPrioritySnapshotEntity;
    }

}