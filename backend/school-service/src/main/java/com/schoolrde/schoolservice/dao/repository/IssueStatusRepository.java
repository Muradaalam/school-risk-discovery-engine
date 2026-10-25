package com.schoolrde.schoolservice.dao.repository;


import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;

import com.schoolrde.schoolservice.entity.IssueStatus;

public interface IssueStatusRepository extends JpaRepository<IssueStatus,Integer>{
    
	Optional<IssueStatus> findById(Integer Id);
    
}
