package com.schoolrde.schoolservice.dao.repository;

import java.util.List;
import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;

import com.schoolrde.schoolservice.entity.TenderEntity;


public interface TenderRepository extends JpaRepository<TenderEntity,Integer>{
    
	Optional<TenderEntity> findById(Integer Id);
	
	List<TenderEntity> findByProjectId(Integer projectId);
    
	boolean existsByTenderNumber(String tenderNumber);
	
}