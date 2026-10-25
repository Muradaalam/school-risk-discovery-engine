package com.schoolrde.schoolservice.dao.repository;

import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;

import com.schoolrde.schoolservice.entity.ProjectEntity;

public interface ProjectRepository extends JpaRepository<ProjectEntity,Integer>{
    
	Optional<ProjectEntity> findById(Integer Id);
    
}
