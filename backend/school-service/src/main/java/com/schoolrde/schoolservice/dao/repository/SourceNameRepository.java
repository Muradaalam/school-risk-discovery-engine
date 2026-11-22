package com.schoolrde.schoolservice.dao.repository;


import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;

import com.schoolrde.schoolservice.entity.SourceName;

public interface SourceNameRepository extends JpaRepository<SourceName,Integer>{
    
	Optional<SourceName> findById(Integer Id);
    
	Optional<SourceName> findBySourceName(String sourceName);
	
}