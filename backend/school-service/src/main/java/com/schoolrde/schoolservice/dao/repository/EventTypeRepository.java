package com.schoolrde.schoolservice.dao.repository;

import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;

import com.schoolrde.schoolservice.entity.EventType;


public interface EventTypeRepository extends JpaRepository<EventType,Integer>{
    
	Optional<EventType> findById(Integer Id);
    
}

