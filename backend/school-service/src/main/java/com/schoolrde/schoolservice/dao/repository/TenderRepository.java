package com.schoolrde.schoolservice.dao.repository;

import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;

import com.schoolrde.schoolservice.entity.TenderEntity;


public interface TenderRepository extends JpaRepository<TenderEntity,Integer>{
    
	Optional<TenderEntity> findById(Integer Id);
    
}