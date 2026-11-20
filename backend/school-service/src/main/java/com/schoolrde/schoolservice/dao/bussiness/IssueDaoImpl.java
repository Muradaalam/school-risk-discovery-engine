package com.schoolrde.schoolservice.dao.bussiness;

import java.util.List;
import java.util.Optional;
import org.springframework.stereotype.Repository;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.schoolrde.schoolservice.dao.repository.IssueRepository;
import com.schoolrde.schoolservice.entity.IssueEntity;
import com.schoolrde.schoolservice.util.JsonUtility;

@Repository
public class IssueDaoImpl implements IssueDao{

    private static final Logger LOGGER = LoggerFactory.getLogger(IssueDaoImpl.class);

    private final IssueRepository issueRepository;

    public IssueDaoImpl(IssueRepository issueRepository){
        this.issueRepository=issueRepository;
    }

    @Override
    public List<IssueEntity> findIssueBySchoolId(Integer schoolId){
        LOGGER.info("Quering issue from database with schoolId : {}", schoolId);
        return issueRepository.findBySchoolId(schoolId);
    }

    @Override
    public Optional<IssueEntity> findIssueById(Integer id){
        LOGGER.info("Quering issue from database with id : {}", id);
        return issueRepository.findById(id);
    }

    @Override
    public IssueEntity saveIssue(IssueEntity issueEntity){
        LOGGER.info("issue to be saved into DB : {}", JsonUtility.toJson(issueEntity));
        IssueEntity savedIssueEntity=issueRepository.save(issueEntity);
        LOGGER.info("issue saved successfully : {}", JsonUtility.toJson(savedIssueEntity));
        return savedIssueEntity;
    }

}
