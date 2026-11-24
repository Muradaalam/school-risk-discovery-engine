package com.schoolrde.schoolservice.dao.repository;

import java.util.List;
import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;

import com.schoolrde.schoolservice.entity.EventEntity;


public interface EventRepository extends JpaRepository<EventEntity,Integer>{
    
	Optional<EventEntity> findById(Integer Id);
    
	List<EventEntity> findBySchoolId(Integer schoolId);
}
