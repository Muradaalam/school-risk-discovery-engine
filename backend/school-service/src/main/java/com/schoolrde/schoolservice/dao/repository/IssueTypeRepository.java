package com.schoolrde.schoolservice.dao.repository;


import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;

import com.schoolrde.schoolservice.entity.IssueType;

public interface IssueTypeRepository extends JpaRepository<IssueType,Integer>{
    
	Optional<IssueType> findById(Integer Id);
    
}
