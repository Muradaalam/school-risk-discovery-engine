package com.schoolrde.schoolservice.dao.bussiness;

import java.util.List;
import java.util.Optional;
import org.springframework.stereotype.Repository;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.schoolrde.schoolservice.dao.repository.TenderRepository;
import com.schoolrde.schoolservice.entity.TenderEntity;
import com.schoolrde.schoolservice.util.JsonUtility;

@Repository
public class TenderDaoImpl implements TenderDao{

    private static final Logger LOGGER = LoggerFactory.getLogger(TenderDaoImpl.class);

    private final TenderRepository tenderRepository;

    public TenderDaoImpl(TenderRepository tenderRepository){
        this.tenderRepository=tenderRepository;
    }

    @Override
    public List<TenderEntity> findTenderByProjectId(Integer projectId){
        LOGGER.info("Quering tender from database with projectId : {}", projectId);
        return tenderRepository.findByProjectId(projectId);
    }

    @Override
    public Optional<TenderEntity> findTenderById(Integer id){
        LOGGER.info("Quering tender from database with id : {}", id);
        return tenderRepository.findById(id);
    }

    @Override
    public TenderEntity saveTender(TenderEntity tenderEntity){
        LOGGER.info("tender to be saved into DB : {}", JsonUtility.toJson(tenderEntity));
        TenderEntity savedTenderEntity=tenderRepository.save(tenderEntity);
        LOGGER.info("tender saved successfully : {}", JsonUtility.toJson(savedTenderEntity));
        return savedTenderEntity;
    }

}
