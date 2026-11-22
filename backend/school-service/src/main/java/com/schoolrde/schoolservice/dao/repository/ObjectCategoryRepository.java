package com.schoolrde.schoolservice.dao.repository;


import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;

import com.schoolrde.schoolservice.entity.ObjectCategory;

public interface ObjectCategoryRepository extends JpaRepository<ObjectCategory,Integer>{
    
	Optional<ObjectCategory> findById(Integer Id);
    
}