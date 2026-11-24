package com.schoolrde.schoolservice.dao.bussiness;

import java.util.List;
import java.util.Optional;

import com.schoolrde.schoolservice.entity.IssueEntity;

public interface IssueDao{
    IssueEntity saveIssue(IssueEntity issue);

    List<IssueEntity> findIssueBySchoolId(Integer schoolId);

    Optional<IssueEntity> findIssueById(Integer id);

}
