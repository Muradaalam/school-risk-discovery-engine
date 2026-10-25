package com.schoolrde.schoolservice.dao.repository;

import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;

import com.schoolrde.schoolservice.entity.TenderStatus;

public interface TenderStatusRepository extends JpaRepository<TenderStatus,Integer>{
    
	Optional<TenderStatus> findById(Integer Id);
    
}
