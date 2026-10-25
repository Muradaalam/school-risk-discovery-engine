package com.schoolrde.schoolservice.dao.repository;

import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;

import com.schoolrde.schoolservice.entity.IssueEntity;


public interface IssueRepository extends JpaRepository<IssueEntity,Integer>{
    
	Optional<IssueEntity> findById(Integer Id);
    
}